import numpy as np

def lvl_2_sum(array_store, neue_werte_array, summed_array, sum_case, zeilen, double_effects, effects):
    if sum_case == 1:
        lvl_2_factors = np.zeros((zeilen, double_effects * 3))  # array for effects

        lvl_2_factors[:, 0] = summed_array[:, effects - double_effects]
        lvl_2_factors[:, 1] = array_store[:, effects - double_effects]
        lvl_2_factors[:, 2] = neue_werte_array[:, effects - double_effects]
        lvl_2_factors[:, 3] = summed_array[:, effects - double_effects + 1]
        lvl_2_factors[:, 4] = array_store[:, effects - double_effects + 1]
        lvl_2_factors[:, 5] = neue_werte_array[:, effects - double_effects + 1]

    return lvl_2_factors
