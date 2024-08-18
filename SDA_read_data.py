import numpy as np


def sda_read(world):


    # Extraction of demand matrix Y
    m_Y_raw = world.Y.iloc[:, :]
    m_Y = m_Y_raw.values
    print(m_Y)
    v_Y_sum1 = np.sum(m_Y, axis=1)

    # Extraction of THG
    m_CO2_raw = world.E.iloc[0, :]  # line CO2
    m_CH4_raw = world.E.iloc[1, :]  # line C4
    m_N2O_raw = world.E.iloc[2, :]  # line N2O
    m_SF6_raw = world.E.iloc[3, :]  # line SF6
    m_FG_raw = world.E.iloc[4, :]  # line Fgase
    m_CO2 = m_CO2_raw.values
    m_CH4 = m_CH4_raw.values
    m_N2O = m_N2O_raw.values
    m_SF6 = m_SF6_raw.values
    m_FG = m_FG_raw.values
    m_all_THG = np.vstack((m_CO2, m_CH4, m_N2O, m_SF6, m_FG))
    #print("mTHG: ")
    #print(m_all_THG)
    all_units = world.units['Satellite account']
    units_ext_raw = all_units.iloc[:, 0]
    units_ext = units_ext_raw.values.reshape(-1, 1)
    #print(units_ext)
    #all_ext = world.get_index('Satellite account')
    #print(all_ext)
    all_ext = ['CO2', 'CH4', 'N2O', 'SF6', 'F-Gase']
    name_ext_raw = [item[0] for item in all_ext]
    name_ext = np.reshape(name_ext_raw, (-1, 1))
    #print(name_ext)
    m_all_THG_units = np.hstack((name_ext, units_ext, m_all_THG))

    # converting in T CO2eq
    m_all_THG_units[:, 1] = 'T CO2eq'  # new unit
    m_all_THG_units[0, 2:] *= (0.001)  # kg in T
    m_all_THG_units[1, 2:] *= (0.027)  # kg in T, CH4 in CO2eq
    m_all_THG_units[2, 2:] *= (0.273)  # kg in T, N20 in CO2eq
    m_all_THG_units[3, 2:] *= (25.200)  # kg in T, SF6 in CO2eq
    m_all_THG_units[4, 2:] *= (0.001)  # kg in T
    #print(m_all_THG_units.shape)
    #print("mTHGunits")
    #print(m_all_THG_units)

    # sum GHG: THG in CO2eq per sector, per region
    m_all_THG_eq = m_all_THG_units[:, 2:] #without units
    v_env = np.sum(m_all_THG_eq, axis=0)
    v_env = v_env.reshape(1, -1)
    v_env = v_env.flatten()  # Dies macht aus v_env ein eindimensionales Array.
    #print(v_env)
    #print(v_env.shape)


    # Direct extraction of L
    m_L_raw = world.w.iloc[:, :]
    m_L1 = m_L_raw.values


    #alculation of production x
    v_X_calc2 = m_L1 @ v_Y_sum1
    v_X_calc2 = np.array(v_X_calc2)
    #print("x calc")
    #print(v_X_calc2)
    #print(v_X_calc2.shape)


    # calculation of environmental diagonal matrix
    #non_zero_indices = v_X_calc2 != 0
    non_zero_indices = v_X_calc2 != 0
    v_e = np.zeros_like(v_env)
    v_e[non_zero_indices] = v_env[non_zero_indices] / v_X_calc2[non_zero_indices]
    #print(v_e)
    m_e = np.diag(v_e.flatten())

    m_c1 = m_L1 @ m_Y
    m_c = m_e @ m_c1

    #print(v_c)

    #return v_c, m_e, m_L1, v_Y_sum1
    return m_c, m_e, m_L1, m_Y, m_all_THG_units

