import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider, CheckButtons


# The parametrized function to be plotted
def f(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    harmonic = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    if show_noise:
        noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), size=len(t))
        return harmonic + noise
    else:
        return harmonic


t = np.linspace(0, 1, 1000)

# Define initial parameters
initial_amplitude = 1.0
initial_frequency = 1.0
initial_phase = 0.0
initial_noise_mean = 0.0
initial_noise_covariance = 0.0
initial_show_noise = True
# Create the figure and the line that we will manipulate
fig, ax = plt.subplots(figsize=(14, 6))
line, = ax.plot(t, f(t, initial_amplitude, initial_frequency, initial_phase, initial_noise_mean,
                     initial_noise_covariance, initial_show_noise), lw=2)

# adjust the main plot to make room for the sliders
fig.subplots_adjust(bottom=0.3)

# Make slider to control the frequency.
ax_freq = fig.add_axes([0.1, 0.01, 0.65, 0.03])
freq_slider = Slider(
    ax=ax_freq,
    label='Frequency [Hz]',
    valmin=0,
    valmax=10,
    valinit=initial_frequency,
)

# Make slider to control the amplitude
ax_amp = fig.add_axes([0.1, 0.06, 0.65, 0.03])
amplitude_slider = Slider(
    ax=ax_amp,
    label="Amplitude",
    valmin=0,
    valmax=10,
    valinit=initial_amplitude
)
ax_phase = fig.add_axes([0.1, 0.11, 0.65, 0.03])
phase_slider = Slider(
    ax=ax_phase,
    label="Phase",
    valmin=0,
    valmax=2*np.pi,
    valinit=initial_phase
)
ax_noise_mean = fig.add_axes([0.1, 0.16, 0.65, 0.03])
noise_mean_slider = Slider(
    ax=ax_noise_mean,
    label="Noise mean",
    valmin=-1,
    valmax=1,
    valinit=initial_noise_mean
)
ax_noise_covariance = fig.add_axes([0.1, 0.21, 0.65, 0.03])
noise_covariance_slider = Slider(
    ax=ax_noise_covariance,
    label="Noise covariance",
    valmin=0,
    valmax=1,
    valinit=initial_noise_covariance
)


# Create a button to reset the sliders to initial values.
ax_reset = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button_reset = Button(ax_reset, 'Reset', hovercolor='0.975')

# Create checkbutton to toggle noise
ax_noise_toggle = fig.add_axes([0.8, 0.15, 0.1, 0.04])
noise_toggle_button = CheckButtons(ax=ax_noise_toggle, labels=['Show noise'], actives=[initial_show_noise])
def toggle_noise(label):
    update(None)

# The function to be called anytime a slider's value changes
def update(val):
    line.set_ydata(f(t, amplitude_slider.val, freq_slider.val, phase_slider.val, noise_mean_slider.val,
                     noise_covariance_slider.val, noise_toggle_button.get_status()[0]))
    fig.canvas.draw_idle()

# register the update function with each slider
freq_slider.on_changed(update)
amplitude_slider.on_changed(update)
phase_slider.on_changed(update)
noise_mean_slider.on_changed(update)
noise_covariance_slider.on_changed(update)
noise_toggle_button.on_clicked(toggle_noise)

def reset(event):
    freq_slider.reset()
    amplitude_slider.reset()
    phase_slider.reset()
    noise_mean_slider.reset()
    noise_covariance_slider.reset()
    noise_toggle_button.set_active(True)
button_reset.on_clicked(reset)



plt.show()