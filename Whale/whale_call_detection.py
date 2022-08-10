# internal python libraries
from copy import copy

# 3rd party libraries
import numpy as np
from scipy.signal import spectrogram as sp

# internally developed methods
import grouper_bfs as gp


large_kernel_45 = np.array([[0, 1, 2, 3, 4, 5, 6],
                            [-1, 0, 1, 2, 3, 4, 5],
                            [-2, -1, 0, 1, 2, 3, 4],
                            [-3, -2, -1, 0, 1, 2, 3],
                            [-4, -3, -2, -1, 0, 1, 2],
                            [-5, -4, -3, -2, -1, 0, 1],
                            [-6, -5, -4, -3, -2, -1, 0]])

blue_whale_call_statistics = {'min_freq': 40,
                              'max_freq': 55,
                              'time diff': 180,
                              'frequency diff': 2}


def sub_matrix_generator(matrix, sub_matrix_shape):
    """Runs horizontally first, then vertically"""
    for x in range(matrix.shape[0] - (sub_matrix_shape[0] - 1)):
        for y in range(matrix.shape[1] - (sub_matrix_shape[1] - 1)):
            yield x, y, matrix[x:x + sub_matrix_shape[0], y:y + sub_matrix_shape[0]]


def convolve(matrix, kernel):
    kernelized_matrix = np.zeros((matrix.shape[0] - (kernel.shape[0] - 1), matrix.shape[1] - (kernel.shape[1] - 1)))
    generator = sub_matrix_generator(matrix, kernel.shape)
    for x_pos, y_pos, sub_matrix in generator:
        kernelized_matrix[x_pos, y_pos] = (sub_matrix * kernel).sum()
    return kernelized_matrix


def detect_whale_call_from_audio(audio_data, audio_frequency, whale_statistics_dict=blue_whale_call_statistics,
                                 conv_kernel=large_kernel_45, min_group_size=300, quantile_threshold=0.95):
    freq, t, spec = sp(audio_data, fs=audio_frequency, window='hanning', nperseg=8000, noverlap=7920)
    freq_filter = (whale_statistics_dict['min_freq'] <= freq) & (freq <= whale_statistics_dict['max_freq'])
    spec = spec[freq_filter, :]

    # kernelize spectrogram
    kernelized_spec = convolve(spec, conv_kernel)

    # scale the output
    kernelized_spec = (kernelized_spec - kernelized_spec.min()) / (kernelized_spec.max() - kernelized_spec.min())

    # filter results
    filtered_kspec = copy(kernelized_spec)
    quantile_band = np.quantile(kernelized_spec, quantile_threshold)  # 0.95
    filtered_kspec[filtered_kspec < quantile_band] = 0
    filtered_kspec[filtered_kspec > quantile_band] = 1

    # build groups
    groups = gp.group_array(filtered_kspec, threshold=0.95)

    # filter out small groups
    large_groups = [g for g in groups if len(g.group_members()) > min_group_size]
    x = np.arange(len(large_groups))
    group_dict = {num + 1: group for group, num in zip(large_groups, x)}

    # build walking means of each group
    walking_medians = {key: value.walking_median() for key, value in group_dict.items()}

    # smooth the walking means
    smooth_medians = {key: gp.moving_average(np.array(value), 10) for key, value in walking_medians.items()}

    # compute statistics
    statistics_dict = {}
    for key, value in smooth_medians.items():
        if len(value) > 0:
            statistics_dict[key] = gp.group_statistics(value)

    for key, value in statistics_dict.items():
        if (statistics_dict[key]['time diff'] > whale_statistics_dict['time diff'] and
                statistics_dict[key]['frequency diff'] > whale_statistics_dict['frequency diff']):
            return True
    return False
