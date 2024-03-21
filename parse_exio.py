import numpy as np
from mario import parse_exiobase_3,slicer

def sda_parse(year, exio_path):


    path1 = exio_path+'IOT_' + str(year) + '_ixi.zip'   # parsing of year X
    world = parse_exiobase_3(path=path1, calc_all=True)


    # Extraction of transaction coefficients matrix A
    m_A_raw = world.z.iloc[:, :]
    m_A = m_A_raw.values
    # print(m_A)


    # Extraction of demand matrix Y
    m_Y_raw = world.Y.iloc[:, :]
    m_Y = m_Y_raw.values
    #print(m_Y)
    v_Y_sum1 = np.sum(m_Y, axis=1)
    #print(m_Y_sum1)

    # Direct extraction of L
    m_L_raw = world.w.iloc[:, :]
    m_L1 = m_L_raw.values

    # Definition of Identity matrix
    n = m_L1.shape[1]
    m_I = np.eye(n)
    # print(m_I)

    # Calculation of Leontief Inverser L
    #m_L_non_inv = m_I - m_A
    #m_L = np.linalg.inv(m_L_non_inv)
    #print(m_L)

    m_X_raw = world.iloc[:, :]
    v_X = m_X_raw.values
    print(v_X)


    # Calculation of production x
    #v_X_calc = m_L1 @ v_Y_sum1
    # print(v_X_calc2)




    # Calculation of THG emission vector
    m_c1 = m_L1 @ v_Y_sum1
    v_c = m_e @ m_c1



