#!/usr/bin/env python

import numpy as np


def hw01(S1, S2):
    """
    S1: the answer
    S2: the formula student inputs
    In this part, we have two kinds of formula:
    - all operators are times(*) and divide(/)
    - using function of VLOOKUP
    """

    # make both stings to lower case
    s1 = S1.lower()
    s2 = S2.lower()

    # kick out '=' symbol and space
    s1 = s1.strip('=')
    s1 = s1.strip()
    s2 = s2.strip('=')
    s2 = s2.strip()

    # start comparing
    if s1 == s2:
        return True
    elif 'vlookup' in s1:
        # get the parameters of VLOOKUP function
        s1_split = s1.lstrip('=vlookup(')
        s1_split = s1_split.rstrip(')')
        s2_split = s2.lstrip('=vlookup(')
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
        s1_split = s1.lstrip('=mmult(')
        s1_split = s1_split.rstrip(')')
        s2_split = s2.lstrip('=mmult(')
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
        return False