import matplotlib.pyplot as plt
import numpy as np

def plot_stamp(ta, tb, matrix_profile, indexes, m):
    fig_width = 16
    fig_height = 10
    fig_dpi = 100
    plt.figure(figsize=(fig_width, fig_height), dpi=fig_dpi)
    fig = plt.subplots(nrows=4, ncols=1)
    plt.tight_layout()

    plt.subplot(411)
    plt.plot(ta)
    plt.xlim((0, len(ta)))
    plt.title('TimeSeries A')

    plt.subplot(412)
    plt.plot(tb)
    plt.plot(range(np.argmax(matrix_profile), np.argmax(matrix_profile) + m),
             tb[np.argmax(matrix_profile):np.argmax(matrix_profile) + m], c='r')
    plt.plot(range(np.argmin(matrix_profile), np.argmin(matrix_profile) + m),
             tb[np.argmin(matrix_profile):np.argmin(matrix_profile) + m], c='k')
    plt.title('TimeSeries B')
    plt.xlim((0, len(tb)))

    plt.subplot(413)
    plt.title('Matrix Profile AB')
    plt.plot(range(0, len(matrix_profile)), matrix_profile, '#ff5722')
    plt.plot(np.argmax(matrix_profile), np.max(matrix_profile), marker='x', ms=10)
    plt.plot(np.argmin(matrix_profile), np.min(matrix_profile), marker='*', ms=10, c='k')
    plt.xlim((0, len(tb)))

    plt.subplot(414)
    plt.title('Matrix Profile Index')
    plt.plot(indexes, '#ff5722')
    plt.xlim((0, len(tb)))

    plt.show()

def motif(ta, matrix_profile, indexes, m):
    fig_width = 16
    fig_height = 10
    fig_dpi = 100
    plt.figure(figsize=(fig_width, fig_height), dpi=fig_dpi)
    fig = plt.subplots(nrows=4, ncols=1)
    plt.tight_layout()

    #####################    1     ###################
    plt.subplot(411)
    plt.plot(ta)
    plt.xlim((indexes[np.argmax(matrix_profile)],indexes[np.argmax(matrix_profile)] + m ))
    plt.title('motif in ta')
    ####################     2     ###################

    ###################     3     #####################
    plt.subplot(413)


    plt.title('discord a')
    plt.plot(ta)
    plt.xlim((indexes[np.argmin(matrix_profile)], indexes[np.argmin(matrix_profile)] + m))
    ##################      4      ######################

    ####################################################
    plt.show()

