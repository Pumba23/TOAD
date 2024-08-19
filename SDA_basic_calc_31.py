
import numpy as np

import math
#from SDA_LMDI_new import SDA_LMDI
from SDA_basic_DL81 import SDA_LMDI
from SDA_basic_DL61 import SDA_LMDI_pl
import os
import datetime
from SDA_result_summation import m_sum

#include intermediate imports! whole L -- ganze matrizen nehmen und teile ausnullen

def SDA_calc_new3(m_c_0, m_e_0, m_L_0, m_Y_0, m_c_t, m_e_t, m_L_t, m_Y_t, num_regions_0, num_sectors_0, reg_to_reg_type, pop_0, pop_t, dl):

    eps1 = 0.00000000000000001  # small value for avoiding 0
    eps2 = 0.000000000000000011
    now = datetime.datetime.now()
    date_str = now.strftime("%H-%M_%d-%m-%Y")
    total = 1


    list_factors_0 = [m_e_0, m_L_0, m_Y_0]
    names_factors = ['Emission intensity', 'Structure', 'Activity']
    num_factors = len(list_factors_0)


    m_results_11 = np.zeros((num_sectors_0, num_factors))
    m_results_12 = np.zeros((num_sectors_0, num_factors))
    m_results_21 = np.zeros((num_sectors_0, num_factors))
    m_results_22 = np.zeros((num_sectors_0, num_factors))

    Cct1 = 1
    Cct2 = 1
    m_Y_t_21 = 1


    if reg_to_reg_type == 'dom1':
        case = 7
    if reg_to_reg_type == 'from1to2':
        case = 6
    if reg_to_reg_type == 'from2to1':
        case = 5
    if reg_to_reg_type == 'dom2':
        case = 4
    if reg_to_reg_type == 'pb':
        case = 3
    if reg_to_reg_type == 'cb':
        case = 2
    if reg_to_reg_type == 'saldo':
        case = 1


    if case in [7]:  # dom1
        m_e_0_11 = np.copy(m_e_0)
        m_e_t_11 = np.copy(m_e_t)
        m_Y_0_11 = np.copy(m_Y_0)
        m_Y_t_11 = np.copy(m_Y_t)

        for i in range(0, 9):  # exclusive 9
            m_e_0_11[i + 9, i + 9] = 0
            m_e_t_11[i + 9, i + 9] = 0

        Cet1 = m_e_0_11
        Cet2 = m_e_t_11

        CLt1 = m_L_0
        CLt2 = m_L_t

        for i in range(0, 9):  # exclusive 9; nur y11 demand
            m_Y_0_11[i, 1] = 0
            m_Y_t_11[i, 1] = 0
            m_Y_0_11[i + 9, 1] = 0
            m_Y_t_11[i + 9, 1] = 0
            m_Y_0_11[9 + i, 0] = 0
            m_Y_t_11[9 + i, 0] = 0

        Cyt1 = m_Y_0_11
        Cyt2 = m_Y_t_11

        cut = 11

        m_results_11, tag = SDA_LMDI(Cct1, Cct2, Cet1, Cet2, CLt1, CLt2, Cyt1, Cyt2, m_results_11, cut)





    if case in [1, 3, 5]:  # exports de
        cut = 21
        m_e_0_21 = np.copy(m_e_0)
        m_e_t_21 = np.copy(m_e_t)
        m_Y_0_21 = np.copy(m_Y_0)
        m_Y_t_21 = np.copy(m_Y_t)

        for i in range(0, 9):  # exclusive 9
            m_e_0_21[i, i] = 0
            m_e_t_21[i, i] = 0

        Cet1 = m_e_0_21
        Cet2 = m_e_t_21

        CLt1 = m_L_0
        CLt2 = m_L_t

        for i in range(0, 9):  # exclusive 9; nur y21 und y11 demand
            m_Y_0_21[i, 1] = 0
            m_Y_t_21[i, 1] = 0
            m_Y_0_21[i + 9, 1] = 0
            m_Y_t_21[i + 9, 1] = 0

        Cyt1 = m_Y_0_21
        Cyt2 = m_Y_t_21

        m_results_21, tag = SDA_LMDI(Cct1, Cct2, Cet1, Cet2, CLt1, CLt2, Cyt1, Cyt2, m_results_21, cut)


    if case in [1, 2, 3, 4]:  # dom2
        m_e_0_22 = np.copy(m_e_0)
        m_e_t_22 = np.copy(m_e_t)
        m_Y_0_22 = np.copy(m_Y_0)
        m_Y_t_22 = np.copy(m_Y_t)

        for i in range(0, 9):  # exclusive 9
            m_e_0_22[i, i] = 0
            m_e_t_22[i, i] = 0

        Cet1 = m_e_0_22
        Cet2 = m_e_t_22

        CLt1 = m_L_0
        CLt2 = m_L_t

        for i in range(0, 9):  # exclusive 9; nur y22 demand
            m_Y_0_22[i, 0] = 0
            m_Y_t_22[i, 0] = 0
            m_Y_0_22[i, 1] = 0
            m_Y_t_22[i, 1] = 0
            m_Y_0_22[9 + i, 0] = 0
            m_Y_t_22[9 + i, 0] = 0

        Cyt1 = m_Y_0_22
        Cyt2 = m_Y_t_22

        cut = 22
        m_results_22, tag = SDA_LMDI(Cct1, Cct2, Cet1, Cet2, CLt1, CLt2, Cyt1, Cyt2, m_results_22, cut)


    if case in [1, 2, 6]:  # imports DE
        m_e_0_12 = np.copy(m_e_0)
        m_e_t_12 = np.copy(m_e_t)
        m_Y_0_12 = np.copy(m_Y_0)
        m_Y_t_12 = np.copy(m_Y_t)

        for i in range(0, 9):  # exclusive 9
            m_e_0_12[i + 9, i + 9] = 0
            m_e_t_12[i + 9, i + 9] = 0

        Cet1 = m_e_0_12
        Cet2 = m_e_t_12

        CLt1 = m_L_0
        CLt2 = m_L_t

        for i in range(0, 9):  # exclusive 9; nur y12 und y22 demand
            m_Y_0_12[i, 0] = 0
            m_Y_t_12[i, 0] = 0
            m_Y_0_12[i + 9, 0] = 0
            m_Y_t_12[i + 9, 0] = 0

        Cyt1 = m_Y_0_12
        Cyt2 = m_Y_t_12

        cut = 12

        m_results_12, tag = SDA_LMDI(Cct1, Cct2, Cet1, Cet2, CLt1, CLt2, Cyt1, Cyt2, m_results_12, cut)


    return m_results_11, m_results_12, m_results_21, m_results_22, num_factors, list_factors_0, names_factors, m_Y_t_21, tag, total
