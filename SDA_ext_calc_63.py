import numpy as np
# from SDA_LMDI_new import SDA_LMDI
from SDA_ext_DL44 import SDA_DL_ext
import os
import datetime


# angepasst an basic DL24 mit pop drin
def SDA_calc_ext(m_c_0, m_e_0, m_L_0, m_Y_0, m_c_t, m_e_t, m_L_t, m_Y_t, num_regions_0, num_sectors_0, reg_to_reg_type,
                 pop_0, pop_t, pop_0_ww, pop_t_ww):

    print("--------------")
    print("hier test welcher regtyp")
    print(reg_to_reg_type)

    #print('calc63')

    names_factors = ['Emission intensity', 'Intermediate trade', 'Overall structure', 'Trade', 'Consumption pattern',
                     'Consumption volume', 'Population']
    num_factors = 7
    tag = 'AAL_63'
    dummy22 = 'yes'

    sum_Y_0_11 = m_Y_0[:, 0].sum()  # alle zeilen
    sum_Y_0_12 = m_Y_0[:9, 1].sum()
    sum_Y_0_21 = m_Y_0[9:, 0].sum()
    sum_Y_0_22 = m_Y_0[:, 1].sum()
    sum_Y_t_11 = m_Y_t[:, 0].sum()
    sum_Y_t_12 = m_Y_t[:9, 1].sum()
    sum_Y_t_21 = m_Y_t[9:, 0].sum()
    sum_Y_t_22 = m_Y_t[:, 1].sum()

    # Erstellen der Einheitsmatrix I mit der gleichen Dimension wie L
    I = np.eye(m_L_0.shape[0])
    L_inv_0 = np.linalg.inv(m_L_0)
    L_inv_t = np.linalg.inv(m_L_t)

    # Berechnung der Input-Koeffizientenmatrix A
    m_A_0 = I - L_inv_0
    m_A_t = I - L_inv_t

    m_T_0 = np.copy(m_A_0)
    m_T_t = np.copy(m_A_t)
    m_B_0 = np.copy(m_Y_0)
    m_B_t = np.copy(m_Y_t)
    m_f_0 = np.copy(m_e_0)
    m_f_t = np.copy(m_e_t)

    # generieren von T
    m_T_0_11 = m_T_0[:9, :9]
    m_T_0_12 = m_T_0[:9, 9:]
    m_T_0_21 = m_T_0[9:, :9]
    m_T_0_22 = m_T_0[9:, 9:]

    m_T_0_up_l = m_T_0_11 + m_T_0_21
    m_T_0_up_r = m_T_0_12 + m_T_0_22
    # print('shape MT')
    # print(m_T_0_up_r.shape)
    m_T_0_up = np.hstack((m_T_0_up_l, m_T_0_up_r))
    m_T_0_star = np.vstack((m_T_0_up, m_T_0_up))
    m_T_0 = m_A_0 / m_T_0_star

    m_T_t_11 = m_T_t[:9, :9]
    m_T_t_12 = m_T_t[:9, 9:]
    m_T_t_21 = m_T_t[9:, :9]
    m_T_t_22 = m_T_t[9:, 9:]

    m_T_t_up_l = m_T_t_11 + m_T_t_21
    m_T_t_up_r = m_T_t_12 + m_T_t_22
    m_T_t_up = np.hstack((m_T_t_up_l, m_T_t_up_r))
    m_T_t_star = np.vstack((m_T_t_up, m_T_t_up))
    m_T_t = m_A_t / m_T_t_star

    # generiere H
    m_H_0 = np.divide(m_A_0, m_T_0, out=np.zeros_like(m_A_0), where=m_T_0 != 0)
    m_H_t = np.divide(m_A_t, m_T_t, out=np.zeros_like(m_A_t), where=m_T_t != 0)

    # print('----------------------L ist ---------------')
    # print((m_L_0))

    #print('----------------------Test T*H ---------------')
    #print((m_H_0 * m_T_0) / m_A_0)

    # generiere p
    m_p_0 = np.zeros((2, 2))
    m_p_0[0, 0] = pop_0_ww
    m_p_0[1, 1] = pop_0

    m_p_t = np.zeros((2, 2))
    m_p_t[0, 0] = pop_t_ww
    m_p_t[1, 1] = pop_t

    # generiere d
    m_d_0 = np.zeros((2, 2))
    m_d_0[0, 0] = sum_Y_0_11 / pop_0_ww
    m_d_0[1, 1] = sum_Y_0_22 / pop_0

    m_d_t = np.zeros((2, 2))
    m_d_t[0, 0] = sum_Y_t_11 / pop_t_ww
    m_d_t[1, 1] = sum_Y_t_22 / pop_t

    # generieren von B

    '''
    divisors0 = np.array([sum_Y_0_11, sum_Y_0_12, sum_Y_0_21, sum_Y_0_22])
    m_B_0[:9, :] /= divisors0[:2]
    m_B_0[9:, :] /= divisors0[2:]

    divisorst = np.array([sum_Y_t_11, sum_Y_t_12, sum_Y_t_21, sum_Y_t_22])
    m_B_t[:9, :] /= divisorst[:2]
    m_B_t[9:, :] /= divisorst[2:]

    '''
    m_B_0[:, 0] = m_B_0[:, 0] / sum_Y_0_11
    m_B_0[:, 1] = m_B_0[:, 1] / sum_Y_0_22

    m_B_t[:, 0] = m_B_t[:, 0] / sum_Y_0_11
    m_B_t[:, 1] = m_B_t[:, 1] / sum_Y_0_22

    m_B_0_11 = m_B_0[:9, 0]
    m_B_0_12 = m_B_0[:9, 1]
    m_B_0_21 = m_B_0[9:, 0]
    m_B_0_22 = m_B_0[9:, 1]

    m_B_0_up_l = m_B_0_11 + m_B_0_21
    m_B_0_up_r = m_B_0_12 + m_B_0_22
    m_B_0_up_l = m_B_0_up_l.reshape(9, 1)
    m_B_0_up_r = m_B_0_up_r.reshape(9, 1)
    m_B_0_up = np.hstack((m_B_0_up_l, m_B_0_up_r))
    m_B_0_star = np.vstack((m_B_0_up, m_B_0_up))
    # print(m_B_0_star.shape)
    m_B_0 = m_Y_0 / m_B_0_star

    m_B_t_11 = m_B_t[:9, 0]
    m_B_t_12 = m_B_t[:9, 1]
    m_B_t_21 = m_B_t[9:, 0]
    m_B_t_22 = m_B_t[9:, 1]

    m_B_t_up_l = m_B_t_11 + m_B_t_21
    m_B_t_up_r = m_B_t_12 + m_B_t_22
    m_B_t_up_l = m_B_t_up_l.reshape(9, 1)
    m_B_t_up_r = m_B_t_up_r.reshape(9, 1)
    m_B_t_up = np.hstack((m_B_t_up_l, m_B_t_up_r))
    m_B_t_star = np.vstack((m_B_t_up, m_B_t_up))
    m_B_t = m_Y_t / m_B_t_star

    m_results_11 = np.zeros((1, num_factors))
    m_results_12 = np.zeros((1, num_factors))
    m_results_21 = np.zeros((1, num_factors))
    m_results_22 = np.zeros((1, num_factors))

    mc = m_c_0

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

        sum1 = 1
        sum2 = 1

        m_Y_0_11 = np.copy(m_Y_0)
        m_Y_t_11 = np.copy(m_Y_t)

        m_B_0_11 = np.copy(m_B_0)
        m_B_t_11 = np.copy(m_B_t)

        m_Y_0_11[:, 0] = m_Y_0_11[:, 0] / sum_Y_0_11
        m_Y_0_11[:, 1] = m_Y_0_11[:, 1] / sum_Y_0_22
        m_Y_t_11[:, 0] = m_Y_t_11[:, 0] / sum_Y_t_11
        m_Y_t_11[:, 1] = m_Y_t_11[:, 1] / sum_Y_t_22

        m_G_0_11 = np.divide(m_Y_0, m_B_0, out=np.zeros_like(m_Y_0), where=m_B_0 != 0)
        m_G_t_11 = np.divide(m_Y_t, m_B_t, out=np.zeros_like(m_Y_t), where=m_B_t != 0)
        m_f_0_11 = np.copy(m_f_0)
        m_f_t_11 = np.copy(m_f_t)
        m_T_0_11 = np.copy(m_T_0)
        m_T_t_11 = np.copy(m_T_t)
        m_H_0_11 = np.copy(m_H_0)
        m_H_t_11 = np.copy(m_H_t)
        m_d_0_11 = np.copy(m_d_0)
        m_d_t_11 = np.copy(m_d_t)

        m_L_0_11 = np.copy(m_L_0)
        m_L_t_11 = np.copy(m_L_t)

        m_p_0_11 = np.copy(m_p_0)
        m_p_t_11 = np.copy(m_p_t)

        for i in range(0, 9):  # exclusive 9
            m_f_0_11[i + 9, i + 9] = 0
            m_f_t_11[i + 9, i + 9] = 0

            m_B_0_11[i, 1] = 0
            m_B_t_11[i, 1] = 0
            m_B_0_11[9 + i, 1] = 0
            m_B_t_11[9 + i, 1] = 0
            m_B_0_11[9 + i, 0] = 0
            m_B_t_11[9 + i, 0] = 0

            m_G_0_11[i, 1] = 0
            m_G_t_11[i, 1] = 0
            m_G_0_11[9 + i, 1] = 0
            m_G_t_11[9 + i, 1] = 0
            m_G_0_11[9 + i, 0] = 0
            m_G_t_11[9 + i, 0] = 0

            m_Y_0_11[i, 1] = 0
            m_Y_t_11[i, 1] = 0
            m_Y_0_11[9 + i, 1] = 0
            m_Y_t_11[9 + i, 1] = 0
            m_Y_0_11[9 + i, 0] = 0
            m_Y_t_11[9 + i, 0] = 0

        # m_d_0_11[1, 1] = 1
        # m_d_t_11[1, 1] = 1
        # m_p_0_11[1, 1] = 1
        # m_p_t_11[1, 1] = 1

        Cet1 = m_f_0_11
        Cet2 = m_f_t_11
        Ctt1 = m_T_0_11
        Ctt2 = m_T_t_11
        Cst1 = m_H_0_11
        Cst2 = m_H_t_11
        Cdt1 = m_d_0_11
        Cdt2 = m_d_t_11
        Cpt1 = m_p_0_11
        Cpt2 = m_p_t_11
        Cbt1 = m_B_0_11
        Cbt2 = m_B_t_11
        Cat1 = m_G_0_11
        Cat2 = m_G_t_11
        Clt1 = m_L_0_11
        Clt2 = m_L_t_11
        Cly1 = m_Y_0_11  # Cyt1
        Cly2 = m_Y_t_11  # Cyt2

        i = 0

        m_results_11, tag = SDA_DL_ext(Clt1, Clt2, Cet1, Cet2, Ctt1, Ctt2, Cst1, Cst2, Cbt1, Cbt2, Cat1, Cat2, Cdt1,
                                       Cdt2, Cpt1, Cpt2, Cly1, Cly2, mc, m_results_11, sum1, sum2, i)

    if case in [1, 3, 5]:  # exports de

        sum1 = 1
        sum2 = 1
        m_B_0_21 = np.copy(m_B_0)
        m_B_t_21 = np.copy(m_B_t)

        m_Y_0_21 = np.copy(m_Y_0)
        m_Y_t_21 = np.copy(m_Y_t)

        m_Y_0_21[:, 0] = m_Y_0_21[:, 0] / sum_Y_0_11
        m_Y_0_21[:, 1] = m_Y_0_21[:, 1] / sum_Y_0_22

        m_Y_t_21[:, 0] = m_Y_t_21[:, 0] / sum_Y_t_11
        m_Y_t_21[:, 1] = m_Y_t_21[:, 1] / sum_Y_t_22

        m_G_0_21 = np.divide(m_Y_0_21, m_B_0, out=np.zeros_like(m_Y_0_21), where=m_B_0 != 0)
        m_G_t_21 = np.divide(m_Y_t_21, m_B_t, out=np.zeros_like(m_Y_t_21), where=m_B_t != 0)
        m_f_0_21 = np.copy(m_f_0)
        m_f_t_21 = np.copy(m_f_t)
        m_T_0_21 = np.copy(m_T_0)
        m_T_t_21 = np.copy(m_T_t)
        m_H_0_21 = np.copy(m_H_0)
        m_H_t_21 = np.copy(m_H_t)
        m_d_0_21 = np.copy(m_d_0)
        m_d_t_21 = np.copy(m_d_t)

        m_L_0_21 = np.copy(m_L_0)
        m_L_t_21 = np.copy(m_L_t)

        m_p_0_21 = np.copy(m_p_0)
        m_p_t_21 = np.copy(m_p_t)

        for i in range(0, 9):  # exclusive 9
            m_f_0_21[i, i] = 0
            m_f_t_21[i, i] = 0

            m_B_0_21[i, 1] = 0
            m_B_t_21[i, 1] = 0
            m_B_0_21[9 + i, 1] = 0
            m_B_t_21[9 + i, 1] = 0

            m_G_0_21[i, 1] = 0
            m_G_t_21[i, 1] = 0
            m_G_0_21[9 + i, 1] = 0
            m_G_t_21[9 + i, 1] = 0

            m_Y_0_21[i, 1] = 0
            m_Y_t_21[i, 1] = 0
            m_Y_0_21[9 + i, 1] = 0
            m_Y_t_21[9 + i, 1] = 0

        # m_d_0_21[1, 1] = 1
        # m_d_t_21[1, 1] = 1
        # m_p_0_21[1, 1] = 1
        # m_p_t_21[1, 1] = 1

        Cet1 = m_f_0_21
        Cet2 = m_f_t_21
        Ctt1 = m_T_0_21
        Ctt2 = m_T_t_21
        Cst1 = m_H_0_21
        Cst2 = m_H_t_21
        Cdt1 = m_d_0_21
        Cdt2 = m_d_t_21
        Cpt1 = m_p_0_21
        Cpt2 = m_p_t_21
        Cbt1 = m_B_0_21
        Cbt2 = m_B_t_21
        Cat1 = m_G_0_21
        Cat2 = m_G_t_21
        Clt1 = m_L_0_21
        Clt2 = m_L_t_21
        Cly1 = m_Y_0_21  # Cyt1
        Cly2 = m_Y_t_21  # Cyt2

        i = 2

        m_results_21, tag = SDA_DL_ext(Clt1, Clt2, Cet1, Cet2, Ctt1, Ctt2, Cst1, Cst2, Cbt1, Cbt2, Cat1, Cat2, Cdt1,
                                       Cdt2, Cpt1, Cpt2, Cly1, Cly2, mc, m_results_21, sum1, sum2, i)

    if case in [1, 2, 3, 4]:  # dom2

        sum1 = 1
        sum2 = 1

        m_B_0_22 = np.copy(m_B_0)
        m_B_t_22 = np.copy(m_B_t)

        m_Y_0_22 = np.copy(m_Y_0)
        m_Y_t_22 = np.copy(m_Y_t)

        m_Y_0_22[:, 0] = m_Y_0_22[:, 0] / sum_Y_0_11
        m_Y_0_22[:, 1] = m_Y_0_22[:, 1] / sum_Y_0_22
        m_Y_t_22[:, 0] = m_Y_t_22[:, 0] / sum_Y_t_11
        m_Y_t_22[:, 1] = m_Y_t_22[:, 1] / sum_Y_t_22

        print('so sieht y aus')
        print(m_Y_0_22)

        m_G_0_22 = np.divide(m_Y_0_22, m_B_0, out=np.zeros_like(m_Y_0_22), where=m_B_0 != 0)
        m_G_t_22 = np.divide(m_Y_t_22, m_B_t, out=np.zeros_like(m_Y_t_22), where=m_B_t != 0)

        m_T_0_22 = np.copy(m_T_0)
        m_T_t_22 = np.copy(m_T_t)

        m_f_0_22 = np.copy(m_f_0)
        m_f_t_22 = np.copy(m_f_t)

        m_H_0_22 = np.copy(m_H_0)
        m_H_t_22 = np.copy(m_H_t)
        m_d_0_22 = np.copy(m_d_0)
        m_d_t_22 = np.copy(m_d_t)

        m_L_0_22 = np.copy(m_L_0)
        m_L_t_22 = np.copy(m_L_t)

        m_p_0_22 = np.copy(m_p_0)
        m_p_t_22 = np.copy(m_p_t)

        print('-------------test B*G --------------')
        print((m_B_0_22 * m_G_0_22) / (m_Y_0_22))

        for i in range(0, 9):  # exclusive 9
            m_f_0_22[i, i] = 0
            m_f_t_22[i, i] = 0

            m_B_0_22[i, 0] = 0
            m_B_t_22[i, 0] = 0
            m_B_0_22[i, 1] = 0
            m_B_t_22[i, 1] = 0
            m_B_0_22[9 + i, 0] = 0
            m_B_t_22[9 + i, 0] = 0

            m_G_0_22[i, 0] = 0
            m_G_t_22[i, 0] = 0
            m_G_0_22[i, 1] = 0
            m_G_t_22[i, 1] = 0
            m_G_0_22[9 + i, 0] = 0
            m_G_t_22[9 + i, 0] = 0

            m_Y_0_22[i, 0] = 0
            m_Y_t_22[i, 0] = 0
            m_Y_0_22[i, 1] = 0
            m_Y_t_22[i, 1] = 0
            m_Y_0_22[9 + i, 0] = 0
            m_Y_t_22[9 + i, 0] = 0

        # m_d_0_22[0, 0] = 1
        # m_d_t_22[0, 0] = 1
        # m_p_0_22[0, 0] = 1
        # m_p_t_22[0, 0] = 1

        Cet1 = m_f_0_22
        Cet2 = m_f_t_22
        Ctt1 = m_T_0_22
        Ctt2 = m_T_t_22
        Cst1 = m_H_0_22
        Cst2 = m_H_t_22
        Cdt1 = m_d_0_22
        Cdt2 = m_d_t_22
        Cpt1 = m_p_0_22
        Cpt2 = m_p_t_22
        Cbt1 = m_B_0_22
        Cbt2 = m_B_t_22
        Cat1 = m_G_0_22
        Cat2 = m_G_t_22
        Clt1 = m_L_0_22
        Clt2 = m_L_t_22
        Cly1 = m_Y_0_22  # Cyt1
        Cly2 = m_Y_t_22  # Cyt2

        i = 3

        m_results_22, tag = SDA_DL_ext(Clt1, Clt2, Cet1, Cet2, Ctt1, Ctt2, Cst1, Cst2, Cbt1, Cbt2, Cat1, Cat2, Cdt1,
                                       Cdt2, Cpt1, Cpt2, Cly1, Cly2, mc, m_results_22, sum1, sum2, i)

    if case in [1, 2, 6]:  # imports DE

        sum1 = 1
        sum2 = 1

        m_B_0_12 = np.copy(m_B_0)
        m_B_t_12 = np.copy(m_B_t)

        m_Y_0_12 = np.copy(m_Y_0)
        m_Y_t_12 = np.copy(m_Y_t)

        m_Y_0_12[:, 0] = m_Y_0_12[:, 0] / sum_Y_0_11
        m_Y_0_12[:, 1] = m_Y_0_12[:, 1] / sum_Y_0_22
        m_Y_t_12[:, 0] = m_Y_t_12[:, 0] / sum_Y_t_11
        m_Y_t_12[:, 1] = m_Y_t_12[:, 1] / sum_Y_t_22

        m_G_0_12 = np.divide(m_Y_0_12, m_B_0, out=np.zeros_like(m_Y_0_12), where=m_B_0 != 0)
        m_G_t_12 = np.divide(m_Y_t_12, m_B_t, out=np.zeros_like(m_Y_t_12), where=m_B_t != 0)

        m_f_0_12 = np.copy(m_f_0)
        m_f_t_12 = np.copy(m_f_t)
        m_T_0_12 = np.copy(m_T_0)
        m_T_t_12 = np.copy(m_T_t)
        m_H_0_12 = np.copy(m_H_0)
        m_H_t_12 = np.copy(m_H_t)
        m_d_0_12 = np.copy(m_d_0)
        m_d_t_12 = np.copy(m_d_t)

        m_L_0_12 = np.copy(m_L_0)
        m_L_t_12 = np.copy(m_L_t)

        m_p_0_12 = np.copy(m_p_0)
        m_p_t_12 = np.copy(m_p_t)

        for i in range(0, 9):  # exclusive 9
            m_f_0_12[i + 9, i + 9] = 0
            m_f_t_12[i + 9, i + 9] = 0

            m_B_0_12[i, 0] = 0
            m_B_t_12[i, 0] = 0
            m_B_0_12[9 + i, 0] = 0
            m_B_t_12[9 + i, 0] = 0

            m_G_0_12[i, 0] = 0
            m_G_t_12[i, 0] = 0
            m_G_0_12[9 + i, 0] = 0
            m_G_t_12[9 + i, 0] = 0

            m_Y_0_12[i, 0] = 0
            m_Y_t_12[i, 0] = 0
            m_Y_0_12[9 + i, 0] = 0
            m_Y_t_12[9 + i, 0] = 0

        # m_d_0_12[0, 0] = 1
        # m_d_t_12[0, 0] = 1
        # m_p_0_12[0, 0] = 1
        # m_p_t_12[0, 0] = 1

        Cet1 = m_f_0_12
        Cet2 = m_f_t_12
        Ctt1 = m_T_0_12
        Ctt2 = m_T_t_12
        Cst1 = m_H_0_12
        Cst2 = m_H_t_12
        Cdt1 = m_d_0_12
        Cdt2 = m_d_t_12
        Cpt1 = m_p_0_12
        Cpt2 = m_p_t_12
        Cbt1 = m_B_0_12
        Cbt2 = m_B_t_12
        Cat1 = m_G_0_12
        Cat2 = m_G_t_12
        Clt1 = m_L_0_12
        Clt2 = m_L_t_12
        Cly1 = m_Y_0_12  # Cyt1
        Cly2 = m_Y_t_12  # Cyt2

        i = 1

        m_results_12, tag = SDA_DL_ext(Clt1, Clt2, Cet1, Cet2, Ctt1, Ctt2, Cst1, Cst2, Cbt1, Cbt2, Cat1, Cat2, Cdt1,
                                       Cdt2, Cpt1, Cpt2, Cly1, Cly2, mc, m_results_12, sum1, sum2, i)

    return m_results_11, m_results_12, m_results_21, m_results_22, num_factors, names_factors, tag, dummy22
