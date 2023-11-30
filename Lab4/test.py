import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider, CheckButtons
from scipy.signal import savgol_filter
import matplotlib.gridspec as gridspec
# The parametrized function to be plotted



# Create time vector
t = np.linspace(0, 2*np.pi, 1000)

def f(t, amplitude, frequency, phase, noise, show_noise):
    harmonic = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    if show_noise:
        return harmonic + noise
    else:
        return harmonic

def create_noise(noise_mean, noise_covariance):
    noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), size=len(t))
    return noise

# Define initial parameters
initial_amplitude = 1.0
initial_frequency = 3.0
initial_phase = 0.0
initial_noise_mean = 0.0
initial_noise_covariance = 0.0
initial_show_noise = True
initial_window_length = 1
initial_polyorder = 0
initial_show_clean_signal = True
initial_show_noisy_signal = False

# Create noise
noise_to_show = create_noise(initial_noise_mean, initial_noise_covariance)

# Create the figure and the line that we will manipulate
fig = plt.figure(figsize=(16, 8))
gs = gridspec.GridSpec(2, 2, height_ratios=[2, 1], width_ratios=[1, 1], hspace=0.2, bottom=0.1)

# Plot the original signal
ax_original = fig.add_subplot(gs[0])
ax_original.set_title('Original signal')
signal = f(t, initial_amplitude, initial_frequency, initial_phase, noise_to_show, initial_show_noise)
# Plot two lines on first subplot
line, = ax_original.plot(t, signal, lw=1, label='Original Signal', color = 'red', zorder=2,
                         visible=initial_show_clean_signal)
line_noisy, = ax_original.plot(t, np.zeros_like(t), lw=1.5, label='Noisy Signal', color='blue', zorder=1,
                               visible=initial_show_noisy_signal)


# Plot the savgol_filter signal
ax_savgol = fig.add_subplot(gs[1], sharey=ax_original)
ax_savgol.set_title('Filtered signal')
filtered_signal = savgol_filter(signal, window_length=initial_window_length, polyorder=initial_polyorder)
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

# Create 2 checkbuttons to toggle clean signal and noisy signal on first subplot
ax_show_clean_signal = fig.add_axes((0.125, 0.9, 0.13, 0.04))
show_clean_signal_button = CheckButtons(ax=ax_show_clean_signal, labels=['Show clean signal'],
                                        actives=[initial_show_clean_signal])

ax_show_noisy_signal = fig.add_axes((0.347, 0.9, 0.13, 0.04))
show_noisy_signal_button = CheckButtons(ax=ax_show_noisy_signal, labels=['Show noisy signal'],
                                        actives=[initial_show_noisy_signal])
def update_clean_signal_visibility(label):
    line.set_visible(show_clean_signal_button.get_status()[0])
    fig.canvas.draw()

def update_noisy_signal_visibility(label):
    line_noisy.set_visible(show_noisy_signal_button.get_status()[0])
    fig.canvas.draw()


show_clean_signal_button.on_clicked(update_clean_signal_visibility)
show_noisy_signal_button.on_clicked(update_noisy_signal_visibility)

def update(val):
    if noise_toggle_button.get_status()[0]:
        signal_noisy = f(t, amplitude_slider.val, freq_slider.val, phase_slider.val,
                         noise_to_show, True)
        signal_clean = f(t, amplitude_slider.val, freq_slider.val, phase_slider.val,
                         noise_to_show, False)
    else:
        signal_noisy = f(t, amplitude_slider.val, freq_slider.val, phase_slider.val,
                         noise_to_show, False)
        signal_clean = signal_noisy

    line.set_ydata(signal_clean)
    line_noisy.set_ydata(signal_noisy)

def update_noise(val):
    global noise_to_show
    if noise_toggle_button.get_status()[0]:
        noise_to_show = create_noise(noise_mean_slider.val, noise_covariance_slider.val)

def update_filtered_signal(val):
    if noise_toggle_button.get_status()[0]:
        data_from_noisy_signal = line_noisy.get_ydata()
        filtered_signal = savgol_filter(data_from_noisy_signal, window_length=int(window_length_slider.val),
                                        polyorder=int(polyorder_slider.val))
        line_savgol.set_ydata(filtered_signal)

    else:
        data_from_signal = line.get_ydata()
        line_savgol.set_ydata(data_from_signal)

    fig.canvas.draw()


# register the update function with each slider and noise button
freq_slider.on_changed(update)
freq_slider.on_changed(update_filtered_signal)
amplitude_slider.on_changed(update)
amplitude_slider.on_changed(update_filtered_signal)
phase_slider.on_changed(update)
phase_slider.on_changed(update_filtered_signal)
noise_mean_slider.on_changed(update)
noise_mean_slider.on_changed(update_filtered_signal)
noise_covariance_slider.on_changed(update)
noise_covariance_slider.on_changed(update_filtered_signal)
noise_toggle_button.on_clicked(update)
noise_toggle_button.on_clicked(update_filtered_signal)
window_length_slider.on_changed(update_filtered_signal)
polyorder_slider.on_changed(update_filtered_signal)
noise_mean_slider.on_changed(update_noise)
noise_covariance_slider.on_changed(update_noise)

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
    if show_clean_signal_button.get_status()[0] == False:
        show_clean_signal_button.set_active(0)
    if show_noisy_signal_button.get_status()[0] == True:
        show_noisy_signal_button.set_active(0)

# Create a button to reset the sliders to initial values.
ax_reset = fig.add_axes((0.8, 0.2, 0.1, 0.04))
button_reset = Button(ax_reset, 'Reset', hovercolor='0.975')

button_reset.on_clicked(reset)

plt.show()