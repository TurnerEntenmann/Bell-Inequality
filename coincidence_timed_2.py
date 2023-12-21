# -*- coding: utf-8 -*-
"""
Simple working example code using Swabian's Time Tagger to collect and print
out count rates on two channels and their coincidence rate

Created on Mon Jan 18 16:38:35 2021

@author: mccambria
"""


# %% Imports


#import TimeTagger
import time, sys
import numpy as np
from CTkMessagebox import CTkMessagebox


# %% Setup


tagger_serial = '1948000SAR'  # Serial number of your Time Tagger
run_time = float(sys.argv[1]) # s (not very precise)
coincidence_window = float(sys.argv[2]) # ns

# Time Tagger hardware channels that your single photon detectors are wired to
hardware_channels = [1, 2]  


## %% Stuff specific to Kolkowitz lab
#
#
#import labrad
#
## Turn on the laser
#with labrad.connect() as cxn:
#    cxn.pulse_streamer.constant([3])
#    
    
# %% Main body



# fxn that is called in epr_state.py and bell_measurement_page.py
def get_counts(run_time, coincidence_window):
    # Connect to the Time Tagger and reset it
    tagger = TimeTagger.createTimeTagger(tagger_serial)
    tagger.reset()
    # Wrap everything else up in a try block so that if something goes wrong
    # we release the tagger and can reconnect to it next time without issues.
    try:
        # Set up a virtual coincidence channel between the hardware channels
        coincidence_window_ps = int(coincidence_window) * 1000
        run_time_ps = int(float(run_time) * (1e12))
        coincidence_channel = TimeTagger.Coincidence(tagger, hardware_channels, 
                                                     coincidence_window_ps)
        
        # Start a countrate measurement using the two hardware channels and the
        # virtual coincidence channel
        channels = [1,2, coincidence_channel.getChannel()]
        measurement = TimeTagger.Countrate(tagger, channels)
        
        # When you set up a measurement, it will not start recording data
        # immediately. It takes some time
        # for the tagger to configure the fpga,
        # etc. The sync call waits until this process is complete. 
        tagger.sync()
        
        measurement.startFor(run_time_ps)
        
        measurement.waitUntilFinished()
            
        # Stop the measurement and record the datapython
        measurement.stop()
        rates = measurement.getData()
        counts = measurement.getCountsTotal()
        
        # Print the results
        print('\n\nHardware channel A: {} counts'.format(counts[0]))
        print('Hardware channel B: {} counts'.format(counts[1]))
        print('Hardware channel A: {} counts per second'.format(rates[0]))
        print('Hardware channel B: {} counts per second'.format(rates[1]))
        print('Coincidences: {} coincidences'.format(counts[2]))
        print('Coincidences: {} coincidences per second'.format(rates[2]),"\n\n")
        
    except Exception as e:
        CTkMessagebox(title=f"Error:\t{e}", message="Could not take data")
        counts = [None, None, None]
        rates = [None, None, None]


    finally:  # Do this even if we crash
        # Release the connection to the Time Tagger
        TimeTagger.freeTimeTagger(tagger)
        print(counts, rates)
        return (counts[0], rates[0], counts[1], rates[1], counts[2], rates[2])


## %% Stuff specific to Kolkowitz lab
#
#
## Turn off the laser
#with labrad.connect() as cxn:
#    cxn.pulse_streamer.constant([])
#while True:
#    timer_func()
#    print('-'*50)