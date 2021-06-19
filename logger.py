#!/usr/bin/env python3
"""Logger module which handles logging data while still printing it to stdout.

This module is intended to replace standard "print" statements by logging the contents of a print statement to a file to keep a record of it while also printing it to stdout. The log is intended to also track the serial of any plot being generated for reference to metadata about plot.

**Author: Jonathan Delgado**

"""
from pathlib import Path
from datetime import datetime
import os
import matplotlib.pyplot as plt


#------------- Initialization -------------#
# Main folder (for logs and plots etc)
MAIN_PATH = Path(__file__).parent / 'logger'
# Path for data folder
DATA_PATH = Path(__file__).parent / 'data'
PLOT_PATH = MAIN_PATH / 'temp'

# Ensure the folders exist for any running
PLOT_PATH.mkdir(exist_ok=True, parents=True)
# Path for log file
LOG_PATH = MAIN_PATH / 'log.txt'
# Serializes this portion of the log, also serves as a flag for indicating
    # whether something new has been logged
SERIAL = None
#------------- End init -------------#


def _serialize():
    """ Generates a unique serial code, useful for file saving to prevent 
        overwriting and conflicts. First portion of the serial code is the date and time requested (ymdHMS), with up to millisecond implementation. This makes the serial code sortable. Useful in creating identifiers for files.
    
        Returns:
            (int): the serial.
    
    """
    # Up to millisecond precision included
    return datetime.now().strftime('%y%m%d%H%M%S%f')[:-3]


def gen_serial():
    """ Requests for a new serial to be generated, updates the log's serial,
        updates the log, then returns the serial.
    
        Returns:
            (int): the new serial
    
    """
    global SERIAL
    SERIAL = _serialize()

    # Every time the serial is updated, it's considered a new entry for the log
    with open(LOG_PATH, 'a') as f:
        # Padding between entries
        # Make sure the file isn't empty for this
        if os.path.getsize(LOG_PATH):
            f.write('\n\n')
        # Write the serial for this log
        f.write(SERIAL + '\n')

    return SERIAL


def log(message):
    """ Saves the message to a log using the active serial. Then prints the
        message to stdout.
        
        Args:
            message (str): the message to be saved and printed.
    
        Returns:
            (None): none
    
    """
    logsilent(message)
    print(message)


def logsilent(message):
    """ Same as log, but does not print to stdout.
        
        Args:
            message (str): the message to be saved.
    
        Returns:
            (None): none
    
    """
    # This is the first log being done.
    if SERIAL == None: gen_serial()

    with open(LOG_PATH, 'a') as f:
        # Write the serial for this log
        f.write(message)
        # Padding between metadata entries
        f.write('\n')


def showfig():
    """ Wrapper to save figure to temp folder with current serial and show it.
    
        Returns:
            (None): none
    
    """
    # This is the first log being done.
    if SERIAL == None: gen_serial()
    
    plot_fname = PLOT_PATH / f'{SERIAL}.pdf'
    # Save the figure
    plt.savefig(plot_fname, bbox_inches='tight')
    plt.show()



#------------- Entry code -------------#


def main():
    ### Testing ###
    log('test')
    log('info1')
    log('info2')

    # run a new log
    new_serial = gen_serial()
    print(new_serial)
    log('new info')

if __name__ == '__main__':
    main()
