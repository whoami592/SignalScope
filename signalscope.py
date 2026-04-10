# ================================================
#          SIGNALSCOPE
#   A Virtual Oscilloscope in Python
#   Coded by: Mr. Sabaz Ali Khan
# ================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import scipy.signal as signal
import csv
from datetime import datetime

# ====================== PARAMETERS ======================
Fs = 10000          # Sampling frequency (Hz)
T = 0.1             # Total time window (seconds)
t = np.arange(0, T, 1/Fs)

# Initial signal parameters
freq = 50.0
amp = 1.0
phase = 0.0
offset = 0.0
noise_level = 0.0
wave_type = 'sine'

# ====================== SIGNAL GENERATOR ======================
def generate_signal(wtype, f, a, p, off, noise):
    if wtype == 'sine':
        sig = a * np.sin(2 * np.pi * f * t + np.deg2rad(p)) + off
    elif wtype == 'square':
        sig = a * signal.square(2 * np.pi * f * t + np.deg2rad(p)) + off
    elif wtype == 'sawtooth':
        sig = a * signal.sawtooth(2 * np.pi * f * t + np.deg2rad(p)) + off
    elif wtype == 'triangle':
        sig = a * signal.sawtooth(2 * np.pi * f * t + np.deg2rad(p), width=0.5) + off
    
    if noise > 0:
        sig += np.random.normal(0, noise, len(t))
    return sig

# ====================== PLOT SETUP ======================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [3, 1]})
fig.suptitle('SIGNALSCOPE - Virtual Oscilloscope\nCoded by Mr. Sabaz Ali Khan', fontsize=16, fontweight='bold', color='#00ff88')

plt.subplots_adjust(left=0.1, bottom=0.35)

line1, = ax1.plot(t*1000, generate_signal(wave_type, freq, amp, phase, offset, noise_level), 
                  lw=2, color='#00ff88')
ax1.set_title('Time Domain Signal', fontsize=14)
ax1.set_xlabel('Time (ms)')
ax1.set_ylabel('Amplitude')
ax1.grid(True, alpha=0.3)
ax1.set_facecolor('#1e1e1e')

line2, = ax2.plot([], [], lw=2, color='#ff8800')
ax2.set_title('Frequency Domain (FFT)', fontsize=14)
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Magnitude')
ax2.grid(True, alpha=0.3)
ax2.set_facecolor('#1e1e1e')

# ====================== SLIDERS ======================
ax_freq = plt.axes([0.15, 0.20, 0.65, 0.03])
ax_amp  = plt.axes([0.15, 0.15, 0.65, 0.03])
ax_phase= plt.axes([0.15, 0.10, 0.65, 0.03])
ax_offset = plt.axes([0.15, 0.05, 0.65, 0.03])
ax_noise = plt.axes([0.15, 0.00, 0.65, 0.03])

s_freq = Slider(ax_freq, 'Frequency (Hz)', 1, 500, valinit=freq, valstep=1)
s_amp  = Slider(ax_amp,  'Amplitude', 0.1, 5.0, valinit=amp)
s_phase= Slider(ax_phase,'Phase (deg)', 0, 360, valinit=phase)
s_offset= Slider(ax_offset,'Offset', -5, 5, valinit=offset)
s_noise = Slider(ax_noise, 'Noise Level', 0, 1, valinit=noise_level)

# ====================== RADIO BUTTONS ======================
rax = plt.axes([0.75, 0.05, 0.15, 0.20])
radio = RadioButtons(rax, ('sine', 'square', 'sawtooth', 'triangle'), active=0)

# ====================== UPDATE FUNCTION ======================
def update(val):
    global wave_type
    sig = generate_signal(wave_type, s_freq.val, s_amp.val, s_phase.val, s_offset.val, s_noise.val)
    line1.set_ydata(sig)
    ax1.set_ylim(sig.min()*1.2, sig.max()*1.2)
    
    # FFT
    fft_vals = np.abs(np.fft.rfft(sig))
    freqs = np.fft.rfftfreq(len(t), 1/Fs)
    line2.set_data(freqs, fft_vals)
    ax2.set_xlim(0, 500)
    ax2.set_ylim(0, fft_vals.max()*1.2)
    
    fig.canvas.draw_idle()

# Connect sliders
s_freq.on_changed(update)
s_amp.on_changed(update)
s_phase.on_changed(update)
s_offset.on_changed(update)
s_noise.on_changed(update)

def radio_func(label):
    global wave_type
    wave_type = label
    update(None)

radio.on_clicked(radio_func)

# ====================== BUTTONS ======================
def export_csv(event):
    sig = generate_signal(wave_type, s_freq.val, s_amp.val, s_phase.val, s_offset.val, s_noise.val)
    filename = f"SignalScope_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Time (ms)', 'Amplitude'])
        for time_val, amp_val in zip(t*1000, sig):
            writer.writerow([round(time_val, 4), round(amp_val, 6)])
    print(f"✅ Exported: {filename}")

def save_plot(event):
    filename = f"SignalScope_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    fig.savefig(filename, dpi=300, facecolor='#111111')
    print(f"✅ Plot saved: {filename}")

ax_export = plt.axes([0.75, 0.75, 0.15, 0.05])
btn_export = Button(ax_export, 'Export CSV', color='#00ff88', hovercolor='#00cc66')
btn_export.on_clicked(export_csv)

ax_save = plt.axes([0.75, 0.68, 0.15, 0.05])
btn_save = Button(ax_save, 'Save Plot', color='#ff8800', hovercolor='#cc6600')
btn_save.on_clicked(save_plot)

# ====================== LAUNCH ======================
plt.style.use('dark_background')
fig.patch.set_facecolor('#111111')
plt.show()

print("🚀 SignalScope started successfully!")
print("   Coded by Mr. Sabaz Ali Khan")