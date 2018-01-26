#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Assessment Statistics

Given a formatted CSV data source, carry out statistical assays and correlations which reveal how performance is distributed and related across questions.

Derived from `randexam` by Matt West and contributors
via a notebook by Aniriduh Madhusadan for CS 101.
Current version by Neal Davis.
'''

exam_path = './exam1.csv'
exclude_list = [ 'davis68','gwang10','ruchark2','brahma2','hychen2','hcheng17','lunanli3','shubham9','xyu37','agmishr2','xtang13' ]

import numpy as np
import pandas as pd
import statistics
import math
from operator import itemgetter

def loadFile( file_path ):
    '''
    Load the file.

    The standard format for the CSV file should have a column with ID data, then the questions in each column, followed by the overall grade.

    Columns may be identified by question name instead of number.

    Return a DataFrame object containing the data.
    '''
    df = pd.read_csv( file_path )
    return df

def clean( df ):
    '''
    Parse through exam data in df, carrying out the following cleaning operations:
    -   removing lines which match exclude_list.
    -   replacing '- ∅ -', RELATE's default "no entry" placeholder and removing
    -   converting percentage strings to floats

    Return a DataFrame without excluded lines.
    '''
    # Remove lines which match exclude_list.
    df = df[ ~df[ 'User ID' ].isin( exclude_list ) ]

    # Replace '- ∅ -', RELATE's default "no entry" placeholder, with np.nan.
    df = df.replace( { '- ∅ -':np.nan } )
    # Remove np.nan-containing entries.
    df = df.dropna()

    # Convert percentage strings to floats.
    n_qs = len( df.columns ) - 2
    for field in df.columns[ 1: ]:
        df[ field ] = df[ field ].str.rstrip('%').astype('float') / 100.0

    return df

def calcStats( df ):
    '''
    Calculate basic statistics for the exam.

    Return a dict containing information in the following fields:
    '''
    results_dict = {}

    results_dict[ 'n_questions' ] = len( df.columns ) - 2
    results_dict[ 'n_students' ]  = len( df )

    overall_col = clean_df[ clean_df.columns[ -1 ] ]
    results_dict[ 'score_min' ]   = overall_col.min()
    results_dict[ 'n_score_min' ] = len( overall_col.loc[ overall_col == overall_col.min() ] )
    results_dict[ 'score_max' ]   = overall_col.max()
    results_dict[ 'n_score_max' ] = len( overall_col.loc[ overall_col == overall_col.max() ] )
    results_dict[ 'score_median' ]= overall_col.median()
    results_dict[ 'score_mean' ]  = overall_col.mean()
    results_dict[ 'score_std' ]   = overall_col.std()

    return results_dict

def reportBasicStats( stats ):
    '''
    Produce a series of plots describing discrimination, difficulty, and other factors.
    '''
    print( f'Number of questions on the exam:    {stats[ "n_questions" ]}' )
    print( f'Number of students taking the exam: {stats[ "n_students" ]}' )
    print( f'Minimum score attained:             {round(stats[ "score_min" ],3)} by {stats[ "n_score_min" ]} students' )
    print( f'Maximum score attained:             {round(stats[ "score_max" ],3)} by {stats[ "n_score_max" ]} students' )
    print( f'Median score on the exam:           {round(stats[ "score_median" ],3)}' )
    print( f'Mean score on the exam:             {round(stats[ "score_mean" ],3)}' )
    print( f'Standard deviation of score:        {round(stats[ "score_std" ],3)}' )

def reportGraphStats( df ):
    '''
    Produce a series of plots describing discrimination, difficulty, and other factors.
    '''
    import matplotlib.pyplot as plt
    import seaborn

    # Plot histogram of all exam question results.
    fig,ax = plt.subplots()
    df.hist()
    #ax.set_title( 'Histogram of Exam Scores' )
    #ax.set_xlabel( 'Scores' )
    #ax.set_ylabel( 'Number of students' )

    # Plot cumulative frequency of overall performance.
    fig,ax = plt.subplots()
    overall_col = df[ df.columns[ -1 ] ]
    sorted_data = overall_col.sort_values()
    ax.step( sorted_data,np.arange( sorted_data.size ),color='g' )
    ax.set_title( 'Cumulative Distribtion of Exam Scores' )
    ax.set_xlabel( 'Scores' )
    ax.set_ylabel( 'Cumulative number of students' )

    # Calculate difficulty.  This method improves on the 0/1 treatment in the original.
    difficulty = {}
    for q in df.columns[ 1:-1 ]:
        difficulty[ q ] = 1.0 - df[ q ].sum() / df[ q ].count()

    # Calculate discrimination.  XXX this is shooting in the dark a bit because of how convoluted randexam's statistics are without documentation.
    overall_col = df[ df.columns[ -1 ] ]
    sorted_data = overall_col.sort_values()

    discrimination = {}
    for q in df.columns[ 1:-1 ]:
        discrimination[ q ] = df[ q ].corr( overall_col )
        #( P_sQ,P_s-P_sQ )

    # Plot difficulty and discrimination indices.
    fig,ax = plt.subplots()
    width = 0.20
    for qi,q in enumerate( df.columns[ 1:-1 ] ):
        rects1 = ax.bar( qi,difficulty[ q ],width,color='g' )
        rects2 = ax.bar( qi+width,discrimination[ q ],width,color='k' )
    ax.set_ylabel( 'Quantity / %' )
    ax.set_xlabel( 'Question label' )
    ax.set_title( 'Question Summary Data' )
    ax.set_xticks( np.arange( len( df.columns[ 1:-1 ] ) )+width / 2)
    ax.set_xticklabels( ( df.columns[ 1:-1 ] ) )
    ax.legend((rects1[0], rects2[0]), ('Difficulty', 'Discrimination Index'))

    # Plot scatterplot of discrimination versus difficulty, the money plot.
    fig, ax = plt.subplots()
    for q in df.columns[ 1:-1 ]:
        x,y = difficulty[ q ],discrimination[ q ]
        ax.scatter( x,y,marker='o',label=q )
        ax.annotate( '%s @ (%s, %s)' % (q,round(x,2),round(y,2)), xy=(x,y), textcoords='data')
    plt.title( 'Scatter Plot of Question Summary Data' )
    plt.xlabel( 'Difficulty D(Q) %' )
    plt.ylabel( 'Discrimination r(Q) %' )
    plt.xlim( ( 0.0,1.0 ) )
    plt.ylim( ( 0.0,1.0 ) )
    plt.legend()

    plt.show()

def main():
    # Load data and calculate number of question.
    exam_df = loadFile( exam_path )

    # Clean data frame by removing extraneous entries (TAs & instructors), etc.
    clean_df = clean( exam_df )

    # Calculate basic statistics and produce a report.
    stats = calcStats( clean_df )
    reportBasicStats( stats )
    reportGraphStats( clean_df )

if __name__ == '__main__':
    main()
