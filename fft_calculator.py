# python3.7.4
# Ird át a saját mappád elérési útjára, készíts egy Data és egy FFT_Results mappát bele!A wb_reader függvényben kell átírni
import os
import cmath
import TestMethods
import numpy as np
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl import load_workbook
from scipy.fftpack import fft
import pandas as pd
import xlsxwriter as xlsw


def matrixFFT(mat):
    numrows, numcols = mat.shape
    headers = [create_header(numcols)]
    matrix = [[0 for i in range(numcols*2+1)] for j in range(numrows)]
    for i, content in mat.iteritems():
        content_list = content.tolist()
        fft_temp = fft(content_list)/numrows*2
        for j in range(0, numrows):
            matrix[j][0] = j
            matrix[j][i+1] = abs(fft_temp[j])
            matrix[j][i+1 + numcols] = cmath.phase(fft_temp[j])
    for i in range(0, numcols):
        matrix[0][i] = matrix[0][i]/2

    matrix = headers+matrix
    return matrix


def create_header(number_cols):
    headers = ['FFT']
    for i in range(0, number_cols):
        col_counter = i+1
        headers.append('abs %s' % col_counter)
    for j in range(0, number_cols):
        col_counter2 = j+1
        headers.append('phase %d' % col_counter2)

    return headers


def write_excel(final_data, root_path, file_name):
    file_name = file_name.split('.')[0]
    root_path_output = os.path.join(root_path, 'FFT_Results/')
    workbook = xlsw.Workbook(
        '%s%s_fft.xlsx' % (root_path_output, file_name))
    worksheet = workbook.add_worksheet()
    for row_num, list_data in enumerate(final_data):
        for col_num, data in enumerate(list_data):
            worksheet.write(row_num, col_num, data)
    workbook.close()
    print('Fájl mentése sikeres')


def wb_reader():
    root_path = 'D:/PROGRAMOZÁS/PYTHON/Motor_analysis/FFT/'
    # Ird át a saját mappád elérési útjára, készíts egy Data és egy FFT_Results mappát bele!
    root_path_input = os.path.join(root_path, 'Data/')
    for root, dirs, files in os.walk(root_path_input):
        for name in files:
            file_path = os.path.join(root, name)
            data = pd.read_excel(file_path, header=None)
            calc_matrix = matrixFFT(data)
            write_excel(calc_matrix, root_path, name)


wb_reader()
