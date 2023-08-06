from typing import List
import pandas as pd
import numpy as np
import os
from errandpy.utility import *

"""
    logファイルのFitting Parameter: a,b,c,dを返します
"""


def write_longfMap_fromlog(x, file_directory, data_shape=(1024, 1024)
                           , isLegacy=False, normMode=1, addtext="", normed=True):
    param_list = [[0, 0, 0, 0]] * data_shape[1]

    files = [file for file in os.listdir(file_directory) if os.path.isfile(os.path.join(file_directory, file))]
    for file in files:
        extension = os.path.splitext(file)[1]
        if extension == ".log":
            # 列の番号
            # 前のSIとこれからのファイル
            num_str = file.split(',')[1].split('.')[0]
            print(num_str)
            if isLegacy:
                param_list[int(num_str) - 1] = legacy_get_logFileParamater(file_directory + file, not normed, normMode=normMode)
            else:
                param_list[int(num_str) - 1] = get_logFileParamater(file_directory + file, not normed, normMode=normMode)

    matrix = np.array(f(x, param_list[0][0], param_list[0][1], param_list[0][2], param_list[0][3]))
    for i in range(1, data_shape[1]):
        array = np.array(f(x, param_list[i][0], param_list[i][1], param_list[i][2], param_list[i][3]))
        matrix = np.concatenate([matrix, array])
    matrix = matrix.reshape(data_shape, order='F')

    data = pd.DataFrame(matrix, index=x)
    data.to_csv("long_map"+addtext+".csv")


def write_shortfMap_fromf_long_csv(f_long_path, f_path, x):
    fdata = pd.read_csv(f_path).values
    fldata = pd.read_csv(f_long_path).values

    fsdata = pd.DataFrame(np.delete(fdata-fldata, 0, 1) ,index=x)
    fsdata.to_csv("short_map.csv")


def csv_to_image(path):
    data = pd.read_csv(path).values
    import matplotlib.pyplot as plt
    plt.imshow(data, cmap='cool')
    plt.colorbar()
    plt.show()


def build_ax(count, figsize=(4, 6)):
    fig = plt.figure(figsize=figsize)
    axes = []
    for i in range(0, count):
        axes.append(fig.add_subplot(count,1,i+1))

    return axes


def f(x, a, b, c, d):
    y = a - b / (c + x) ** d
    return y


def f_legacy(x, a, b, c, d):
    y = a - b / (1 + c * x) ** d
    return y


def force_sphere1(x, HR, c, a):
    # R   = 25
    z = x + c
    y = -HR / 6 / z / z
    return y + a


def force_sphere(x, H, R, c, a):
    # R   = 25
    z = x + c
    y = -2 * H * R ** 3 / (3 * z ** 2) / (z + 2 * R) ** 2
    return y + a


def force_pyramid_square(x, H, theta, c, a):
    return - 2 * H * np.tan(theta) * np.tan(theta) / 3 / (x+c) / np.pi + a


def force_pyramid_sphere(x, H, theta, c, a):
    return - H * np.tan(theta) ** 2 / 6 / (x+c) + a


def force_mixture_guggisberg(x, H, R, theta, c, a):
    z = x + c
    first = R / z
    second = np.tan(theta) ** 2 / (z + R * (1 - np.sin(theta)))
    third = R * (1 - np.sin(theta)) / z / (z + R * (1-np.sin(theta)))
    return - H / 6 * (first + second - third) + a


def force_mixture_zanette(x, H, R, theta, h, L, c, a):
    z = x + c
    b = (z + h) ** 3
    first = h * h * (3 * R * z + (R - z) * h) / z ** 2 / b
    second = L * L / b
    third = 4 * np.tan(theta) * (L + np.tan(theta) * (z + h)) / np.pi / (z + h) ** 2
    return - H / 6 * (first + second + third) + a



def force_mixture_argento(x, H, R, theta, c, a):
    z = x + c
    b = (R + z + R * np.sin(theta))**2
    first = R**2 * (np.sin(theta) - 1) * ((R - z) * np.sin(theta) - R - z)
    second = np.tan(theta) * ((z + R) * np.sin(theta) + R * np.cos(2 * theta))
    return - H / 6 / b * ((first / z / z) - (second / np.cos(theta))) + a









def param_to_legacy(param):
    p = np.copy(param)
    p[1] = param[1] / (param[2] ** param[3])
    p[2] = 1 / param[2]
    return p

def param_from_legacy(param):
    return param_to_legacy(param)



