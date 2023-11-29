import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider, CheckButtons
from scipy.signal import savgol_filter
import matplotlib.gridspec as gridspec

# The parametrized function to be plotted

def f(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    # Генеруємо чистий сигнал
    signal = amplitude * np.sin(2 * np.pi * frequency * t + phase)

    # Генеруємо сигнал з шумом
    noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), size=len(t))
    signal_with_noise = signal + noise

    return signal, signal_with_noise


# Create time vector
t = np.linspace(0, 1, 1000)

# Define initial parameters
initial_amplitude = 1.0
initial_frequency = 3.0
initial_phase = 0.0
initial_noise_mean = 0.0
initial_noise_covariance = 0.0
initial_show_noise = True
initial_window_length = 1
initial_polyorder = 0

# Create the figure and the line that we will manipulate

fig = plt.figure(figsize=(16, 8))
gs = gridspec.GridSpec(2, 2, height_ratios=[2, 1], width_ratios=[1, 1], hspace=0.2, bottom=0.1)

# Plot the original signal
ax_original = fig.add_subplot(gs[0])
ax_original.set_title('Original signal')
signal = f(t, initial_amplitude, initial_frequency, initial_phase, initial_noise_mean, initial_noise_covariance,
           initial_show_noise)
line, = ax_original.plot(t, signal, lw=2, label='Original Signal')
line_with_noise, = ax_original.plot(t, signal, lw=2, color='blue', alpha=0.5, label='Signal with Noise')


# Plot the savgol_filter signal
ax_savgol = fig.add_subplot(gs[1], sharey=ax_original)
ax_savgol.set_title('Filtered signal')
filtered_signal = savgol_filter(signal, window_length=initial_window_length,
                                  polyorder=initial_polyorder)
line_savgol, = ax_savgol.plot(t, filtered_signal, lw=2, label='Savgol Filtered Signal')


# Make slider to control the frequency.
ax_freq = fig.add_axes((0.1, 0.34, 0.65, 0.03))
freq_slider = Slider(ax=ax_freq, label='Frequency [Hz]', valmin=0, valmax=10, valinit=initial_frequency)

# Make slider to control the amplitude
ax_amp = fig.add_axes((0.1, 0.30, 0.65, 0.03))
amplitude_slider = Slider(ax=ax_amp, label="Amplitude", valmin=0, valmax=10, valinit=initial_amplitude)

# Make slider to control the phase
ax_phase = fig.add_axes((0.1, 0.26, 0.65, 0.03))
phase_slider = Slider(ax=ax_phase, label="Phase", valmin=0, valmax=50, valinit=initial_phase)

# Make slider to control the noise
ax_noise_mean = fig.add_axes((0.1, 0.22, 0.65, 0.03))
noise_mean_slider = Slider(ax=ax_noise_mean, label="Noise mean", valmin=-1, valmax=1, valinit=initial_noise_mean)

# Make slider to control the covarianse
ax_noise_covariance = fig.add_axes((0.1, 0.18, 0.65, 0.03))
noise_covariance_slider = Slider(ax=ax_noise_covariance, label="Noise covariance", valmin=0, valmax=1,
                                 valinit=initial_noise_covariance)

# Make slider to control the window length
ax_window_length = fig.add_axes((0.1, 0.14, 0.65, 0.03))
window_length_slider = Slider(ax=ax_window_length, label="Window length", valmin=0, valmax=200, valstep=1,
                              valinit=initial_window_length)

# Make slider to control the window length
ax_polyorder = fig.add_axes((0.1, 0.10, 0.65, 0.03))
polyorder_slider = Slider(ax=ax_polyorder, label="Polyorder", valmin=0, valmax=10, valstep=1, valinit=initial_polyorder)

# Create checkbutton to toggle noise
ax_noise_toggle = fig.add_axes((0.8, 0.28, 0.1, 0.04))
noise_toggle_button = CheckButtons(ax=ax_noise_toggle, labels=['Show noise'], actives=[initial_show_noise])


def update(val):
    clean_signal, signal_with_noise = f(t, amplitude_slider.val, freq_slider.val, phase_slider.val,
                                        noise_mean_slider.val, noise_covariance_slider.val,
                                        show_noise=noise_toggle_button.get_status()[0])

    # Оновлення ліній на графіку
    line.set_ydata(clean_signal)
    line_with_noise.set_ydata(signal_with_noise)
    if noise_toggle_button.get_status()[0]:
        filtered_signal = savgol_filter(signal_with_noise, window_length=int(window_length_slider.val),
                                        polyorder=int(polyorder_slider.val))
        line_savgol.set_ydata(filtered_signal)

    else:
        line_savgol.set_ydata(signal)

    fig.canvas.draw()


# register the update function with each slider and noise button
freq_slider.on_changed(update)
amplitude_slider.on_changed(update)
phase_slider.on_changed(update)
noise_mean_slider.on_changed(update)
noise_covariance_slider.on_changed(update)
noise_toggle_button.on_clicked(update)
window_length_slider.on_changed(update)
polyorder_slider.on_changed(update)

def reset(event):
    freq_slider.reset()
    amplitude_slider.reset()
    phase_slider.reset()
    noise_mean_slider.reset()
    noise_covariance_slider.reset()
    window_length_slider.reset()
    polyorder_slider.reset()
    if noise_toggle_button.get_status()[0] == False:
        noise_toggle_button.set_active(0)


# Create a button to reset the sliders to initial values.
ax_reset = fig.add_axes((0.8, 0.2, 0.1, 0.04))
button_reset = Button(ax_reset, 'Reset', hovercolor='0.975')

button_reset.on_clicked(reset)

plt.show()
