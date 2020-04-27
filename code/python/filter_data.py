import time
import filters
import numpy as np
from scipy.ndimage import convolve1d
from scipy.signal import lfilter

def apply_lowpass(sweep):
    fs = sweep.samp_freq
    num_channels = sweep.num_channels
    num_samples = sweep.num_samples
    channel_data = sweep.channels

    # Generate filter
    filter = filters.lpf_40(fs)
    signal_length = 1125
    #signal_length = len(channel_data[0].raw_data) - len(filter) + 1
    signal_buf = np.empty([num_channels, signal_length], dtype=float)

    sweep.config_filtered_channels(signal_length)

    # Apply filter to raw channel data
    for i in range(sweep.num_channels):
        unfiltered = channel_data[i].raw_data
        #filtered = np.array(np.convolve(unfiltered, filter, mode = 'valid'))
        filtered = lfilter(filter, 1.0, unfiltered)
        signal_buf[i] = filtered

    sweep.set_filtered_channel_data(signal_buf)

    return(sweep)
