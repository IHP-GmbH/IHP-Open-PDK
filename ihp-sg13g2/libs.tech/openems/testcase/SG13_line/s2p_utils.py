import os
import numpy as np
from pylab import *


def readS2P (s2p_name):
    # Read Touchstone S2P file, but only some formats are supported!
    # Files with multiple lines per frequency are not supported
    # 
    # Return value is frequency array and multi-dimension [S] array
    # that can be split like this:
    #   s11 = S[0,0,:]
    #   s12 = S[0,1,:]
    #   s21 = S[1,0,:]
    #   s22 = S[1,1,:]


    s2p_file = open(s2p_name, 'r')
    file_text = s2p_file.readlines()

    f = np.array([])
    s11 = np.array([])
    s21 = np.array([])
    s12 = np.array([])
    s22 = np.array([])

    for line in file_text:
        if ('#' in line):
            # control line
            line = line.strip()     # remove extra spaces
            line = line.upper()     # convert to upper case
            items = line.split()
            freqscale = items[1]    # e.g. GHZ
            datatype = items [2]    # must be S for S-params
            dataformat = items [3]  # e.g. RI
            refimpedance = items [5]

            # frequency scaling
            if   freqscale=='KHZ': freqfactor = 1E3
            elif freqscale=='MHZ': freqfactor = 1E6
            elif freqscale=='GHZ': freqfactor = 1E9
            else: freqfactor = 1

            if (dataformat!='RI' and dataformat!='MA'):
                print ('ERROR: only S-parameter in RI or MA format are supported')
                quit()

            if datatype!='S':
                print ('ERROR: only S-parameter files are supported')
                quit()

        elif ('!' not in line):
            # read data lines, skip comment lines
            items = line.split()
            if len(items)==9:
                freqpoint = float(items[0])
                f = np.append(f,[freqpoint])

                s11a = float(items[1])
                s11b = float(items[2])
                s21a = float(items[3])
                s21b = float(items[4])
                s12a = float(items[5])
                s12b = float(items[6])
                s22a = float(items[7])
                s22b = float(items[8])

                if dataformat=='RI':
                    s11 = np.append(s11, [s11a+s11b*1.j])
                    s21 = np.append(s21, [s21a+s21b*1.j])
                    s12 = np.append(s12, [s12a+s12b*1.j])
                    s22 = np.append(s22, [s22a+s22b*1.j])
                elif dataformat=='MA':
                    s11 = np.append(s11, [s11a*cos(s11b*pi/180) + s11a*sin(s11b*pi/180)*1.j])
                    s21 = np.append(s21, [s21a*cos(s21b*pi/180) + s21a*sin(s21b*pi/180)*1.j])
                    s12 = np.append(s12, [s12a*cos(s12b*pi/180) + s12a*sin(s12b*pi/180)*1.j])
                    s22 = np.append(s22, [s22a*cos(s22b*pi/180) + s22a*sin(s22b*pi/180)*1.j])
                
            else:
                print ('ERROR: number of items in data line does not match (expected 9 items)')
                quit()

    s2p_file.close()

    S = np.array([[s11, s12],[s21, s22]])
    return f, S 

####### end of function readS2P #########


def writeS2P (f, S, s2p_name):
    s11 = S[0,0,:]
    s12 = S[0,1,:]
    s21 = S[1,0,:]
    s22 = S[1,1,:]

    s2p_file = open(s2p_name, 'w')
    s2p_file.write('#   Hz   S  RI   R   50\n')
    s2p_file.write('!\n')
    for index in range(0, len(f)):
        freq = f[index]
        s11re = real(s11[index])
        s11im = imag(s11[index])
        s12re = real(s12[index])
        s12im = imag(s12[index])
        s21re = real(s21[index])
        s21im = imag(s21[index])
        s22re = real(s22[index])
        s22im = imag(s22[index])
        s2p_file.write(str(freq) + ' ' + str(s11re) + ' ' + str(s11im) + ' ' + str(s21re) + ' ' + str(s21im) + ' ' + str(s12re) + ' ' + str(s12im) + ' ' + str(s22re) + ' ' + str(s22im) + '\n')
    s2p_file.close()

####### end of function writeS2P #########

def sxx_to_S (s11, s12, s21, s22):
    S = np.array([[s11, s12],[s21, s22]])
    return S

def S_to_sxx (S):
    s11 = S[0,0,:]
    s12 = S[0,1,:]
    s21 = S[1,0,:]
    s22 = S[1,1,:]
    return s11,s12,s21,s22


def plot_compare (f1, data1, data1label, f2, data2, data2label, yaxistext):
    figure()
    plot(f1/1e9, data1, 'k-', linewidth=2, label=data1label)
    plot(f2/1e9, data2, 'r--', linewidth=2, label=data2label)
    grid()
    legend()
    ylabel(yaxistext)
    xlabel('Frequency (GHz)')    



def plot_S2P_db_phase (f, S):

    s11 = S[0,0,:]
    s12 = S[0,1,:]
    s21 = S[1,0,:]
    s22 = S[1,1,:]

    s11_dB = 20.0*np.log10(np.abs(s11))
    s11_phase = angle(s11, deg=True) 

    s21_dB = 20.0*np.log10(np.abs(s21))
    s21_phase = angle(s21, deg=True) 

    s22_dB = 20.0*np.log10(np.abs(s22))
    s22_phase = angle(s22, deg=True) 

    s12_dB = 20.0*np.log10(np.abs(s12))
    s12_phase = angle(s12, deg=True) 

    # S11,S22 dB
    plot_compare (f, s11_dB, 'S11', f, s22_dB, 'S22', 'S11,S22 [dB]')
    plot_compare (f, s21_dB, 'S21', f, s12_dB, 'S12', 'S21,S12 [dB] ')
    show()



####### end of function plot_S2P_db_phase #########

# filename = 'p:/temp/line_SG13_TM2_over_M1.s2p'
# read S-params
# f, S = readS2P(filename)

# plot S-params
# plot_S2P_db_phase (f, S)
