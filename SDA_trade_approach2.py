import numpy as np
from SDA_result_summation import m_sum


def m_trade(reg_to_reg_type, m_results_11, m_results_12, m_results_21, m_results_22, m_c_0, m_c_t, start, num_factors):



    if reg_to_reg_type == 'dom1':
        if start == 0:
            m_c_sum0 = m_c_0[:9, 0]

        m_c_sum =m_c_t[:9, 0]
        m_results = m_results_11

    if reg_to_reg_type == 'from1to2':
        if start == 0:
            m_c_sum0 = m_c_0[:9, 1]

        m_c_sum =m_c_t[:9, 1]
        m_results = m_results_12

    if reg_to_reg_type == 'from2to1':
        if start == 0:
            m_c_sum0 = m_c_0[9:, 0]

        m_c_sum =m_c_t[9:, 0]

        m_results = m_results_21

    if reg_to_reg_type == 'dom2':
        if start == 0:
            m_c_sum0 = m_c_0[9:, 1]


        m_results = m_results_22
        m_c_sum =m_c_t[9:, 1]

    if reg_to_reg_type == 'pb':
        m_results = m_results_21 + m_results_22
        if start == 0:
            m_c_sum0 = m_c_0[9:, 0] + m_c_0[9:, 1]

        m_c_sum = m_c_t[9:, 0] + m_c_t[9:, 1]

    if reg_to_reg_type == 'cb':
        m_results = m_results_12 + m_results_22
        if start == 0:
            m_c_sum0 = m_c_0[:9, 1] + m_c_0[9:, 1]
        m_c_sum = m_c_t[:9, 1] + m_c_t[9:, 1]
    if reg_to_reg_type == 'saldo':


        m_results = m_results_12 + m_results_22
        m_results = m_results - m_results_21
        if start == 0:
            m_c_sum0 = m_c_0[:9, 1] + m_c_0[9:, 1] - m_c_0[9:, 0]
        m_c_sum = m_c_t[:9, 1] + m_c_t[9:, 1] - m_c_t[9:, 0]


    if start == 0:
        m_c_sum0 = np.array(m_c_sum0).reshape(-1, 1)
        m_c_sum = np.array(m_c_sum).reshape(-1, 1)

        result_zero = np.zeros((9, num_factors))
        m_results = np.hstack([result_zero, m_results])

        return m_results, m_c_sum0, m_c_sum

    else:
        m_c_sum = np.array(m_c_sum).reshape(-1, 1)
        return m_results, m_c_sum