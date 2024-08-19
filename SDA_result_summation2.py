import numpy as np



def m_sum(m_results_years, factors, years):

    numeric_data = m_results_years[:, 1:].astype(float)
    column_sums = np.sum(numeric_data, axis=0)
    arr_with_sums = np.vstack([m_results_years, np.hstack([['sumeffects'], column_sums])])
    print('das hier sind colum sums: ')
    print(column_sums)
    m_print = column_sums.reshape(years+1, factors) #second +1 due to first_zeros

    group_sums = np.array([np.sum(column_sums[i:i + 3]) for i in range(0, len(column_sums), 3)])

    arr_with_group_sums = np.vstack([arr_with_sums, np.hstack(
        [['sumyears'], np.round(group_sums).astype(int), [''] * (len(arr_with_sums[0]) - 1 - len(group_sums))])])


    return arr_with_group_sums, m_print