import numpy as np
import matplotlib.pyplot as plt
def savgol_filter_custom(data, window_size, polyorder):
    half_window = window_size // 2
    filtered_data = np.zeros_like(data)

    for i in range(half_window, len(data) - half_window):
        window_start = i - half_window
        window_stop = i + half_window + 1
        interp_start = i
        interp_stop = i + 1

        window = data[window_start:window_stop]
        coefficients = np.polyfit(np.arange(-half_window, half_window + 1), window, polyorder)
        filtered_data[i] = np.polyval(coefficients, 0)

        _fit_edge(data, window_start, window_stop, interp_start, interp_stop,
                  polyorder, filtered_data)
        
    _fit_edges_polyfit(data, window_size, polyorder, filtered_data)
    return filtered_data

def _fit_edge(x, window_start, window_stop, interp_start, interp_stop,
              polyorder, y):

    x_edge = x[window_start:window_stop]
    poly_coeffs = np.polyfit(np.arange(0, window_stop - window_start),
                             x_edge, polyorder)

    i = np.arange(interp_start - window_start, interp_stop - window_start)
    values = np.polyval(poly_coeffs, i)

    y_edge = y[interp_start:interp_stop]
    y_edge[...] = values
в
def _fit_edges_polyfit(x, window_length, polyorder, y):
    halflen = window_length // 2
    _fit_edge(x, 0, window_length, 0, halflen, polyorder, y)
    n = len(x)
    _fit_edge(x, n - window_length, n, n - halflen, n, polyorder, y)
