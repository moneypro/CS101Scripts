#!/usr/bin/env python

import numpy as np

correctAnswers = {
    "C2": 1e-10,
    "C3": 1e-9,
    "C4": 1e-6,
    "C5": 1e-2,
    "C6": 1e+3,
    "C7": 3.0857e+16,
    "C8": 2.54e-2,
    "C9": 0.3048,
    "C10": 1609.344,
    "C12": 0.3106855961,
    "B15": 3.1415926536,
    "B16": 0
}


def assertSameHw01(S1, S2):
    """
    S1: the answer
    S2: the formula student inputs
    In this part, we have three kinds of formula:
    - all operators are times(*) and divide(/)
    - using function of VLOOKUP (the 2nd parameter must be the minimum table)
    - using function of MMULT
    """

    # make both stings to lower case
    s1 = S1.lower()
    s2 = S2.lower()

    # kick out '=' symbol and space
    s1 = s1.strip('=').strip('\ufeff').replace("'","").replace('"',"").replace('$','')
    s1 = s1.strip()
    s2 = s2.strip('=').strip('\ufeff').replace("'","").replace('"',"").replace('$','')
    s2 = s2.strip()

    # start comparing
    if s1 == s2:
        return True
    elif 'vlookup' in s1:
        # get the parameters of VLOOKUP function
        s1_split = s1.lstrip('vlookup(')
        s1_split = s1_split.rstrip(')')
        s2_split = s2.lstrip('vlookup(')
        s2_split = s2_split.rstrip(')')

        s1_paras = [x.strip() for x in s1_split.split(',')]
        s2_paras = [x.strip() for x in s2_split.split(',')]
        if s1_paras == s2_paras:
            return True
        # VLOOKUP have at most 4 parameters
        if len(s2_paras) > 4:
            return False

        # We check every parameters
        # 1st and 3rd parameter must match
        if s1_paras[0] != s2_paras[0] or s1_paras[2] != s2_paras[2]:
            return False
        # 2nd parameter
        # we assume s1 contains the minimum table which shoule be used
        s1_2nd = s1_paras[1].split(':')
        s2_2nd = s2_paras[1].split(':')
        if s1_2nd[0] < s2_2nd[0] or s1_2nd[1] > s2_2nd[1]:
            return False
        return True
    elif 'mmult' in s1:
        # get the parameters of vlookup function
        s1_split = s1.lstrip('mmult(')
        s1_split = s1_split.rstrip(')')
        s2_split = s2.lstrip('mmult(')
        s2_split = s2_split.rstrip(')')

        s1_paras = [x.strip() for x in s1_split.split(',')]
        s2_paras = [x.strip() for x in s2_split.split(',')]
        if s1_paras == s2_paras:
            return True
        # MMULT have at most 4 parameters
        if s1_paras != s2_paras:
            return False
        return True
    elif '/' in s1:
        # kick out space and parathenses
        pre_s1_split = [x.strip() for x in s1.split('/')]
        pre_s1_split2 = [x.rstrip(')') for x in pre_s1_split]
        s1_split = [x.lstrip('(') for x in pre_s1_split2]
        pre_s2_split = [x.strip() for x in s2.split('/')]
        pre_s2_split2 = [x.rstrip(')') for x in pre_s2_split]
        s2_split = [x.lstrip('(') for x in pre_s2_split2]

        if s1_split == s2_split:
            return True
        # if the answer is correct, we must only contain one divide symbol
        if len(s1_split) != len(s2_split):
            return False
        # for now, each item should be a product of variables
        for i in np.arange(len(s2_split)):
            if '*' in s2_split[i]:
                s1_split2 = [x.strip() for x in s1_split[i].split('*')]
                s1_split2 = [x.strip('(') for x in s1_split2]
                s1_split2 = [x.strip(')') for x in s1_split2]
                s2_split2 = [x.strip() for x in s2_split[i].split('*')]
                s2_split2 = [x.strip('(') for x in s2_split2]
                s2_split2 = [x.strip(')') for x in s2_split2]
                if set(s1_split2) == set(s2_split2):
                    pass
                else:
                    return False
            else:
                if set(s1_split[i]) == set(s2_split[i]):
                    pass
                else:
                    return False
        return True
    # if the answer is correst, it must contain '/'
    else:
        try: 
            if np.isclose(float(s1), float(s2), rtol=2e-2):
                return True
            else:
                return False
        except ValueError:
            return True
