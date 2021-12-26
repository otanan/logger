#!/usr/bin/env python3
"""Logger module which handles logging data while still printing it to stdout.

This module is intended to provide wrappers to functions such as print, plt.showfig, and more, by providing additional functionality such as: saving figures with time-encoding serials along with saving print (now log) messages to a file with the aforementioned serial. This facilitates tying any metadata to its corresponding plot, and saving of test figures for any further review.

**Author: Jonathan Delgado**

"""
from pathlib import Path
from datetime import datetime
import os
import matplotlib.pyplot as plt
# Conversion of functions source to string
import dill.source


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


######################## Serialization ########################


# Getter
def get_serial(): return SERIAL


# Constructor
def _serialize():
    """ Generates a unique serial code, useful for file saving to prevent 
        overwriting and conflicts. First portion of the serial code is the date and time requested (ymdHMS), with up to millisecond implementation. This makes the serial code sortable. Useful in creating identifiers for files.
    
        Returns:
            (int): the serial.
    
    """
    # Up to millisecond precision included
    return datetime.now().strftime('%y%m%d%H%M%S%f')[:-3]


# Setter
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
        _write_header(f)

    return SERIAL


######################## Miscellaneous ########################


def _get_func_source(func):
    """ Gets the source code of the function.
        
        Args:
            func (function): the function of interest.
    
        Returns:
            (str): the source code.
    
    """
    return dill.source.getsource(func).strip()


def _write_header(f):
    """ Prints a header to separate log entries.
        
        Args:
            f (file): the file object (the log) to write to.
    
        Returns:
            (None): none
    
    """
    # A banner to surround the serial
    banner = 80 * '='

    # Padding between entries
    # Make sure the file isn't empty for this
    if os.path.getsize(LOG_PATH):
        f.write('\n\n')

    ### Header writing ###

    # Write the serial in the header for this log
    f.write(banner + '\n')
    f.write(SERIAL + '\n')
    # Print the date and time
    f.write(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '\n')
    f.write(banner + '\n')
    

######################## Logging ########################


def log(message=''):
    """ Saves the message to a log using the active serial. Then prints the
        message to stdout.
        
        Kwargs:
            message (str): the message to be saved and printed. Defaults to an empty string to use an empty log call to print a line for padding.
    
        Returns:
            (None): none
    
    """
    logsilent(message)
    print(message)


def logsilent(message=''):
    """ Same as log, but does not print to stdout.
        
        Args:
            message (str): the message to be saved.
    
        Returns:
            (None): none
    
    """
    # This is the first log being done.
    if SERIAL == None: gen_serial()

    # Check if this is a function trying to be logged
    if callable(message):
        # Convert the function's source code to a string
        message = _get_func_source(message)

    with open(LOG_PATH, 'a') as f:
        # Write the serial for this log
        f.write(str(message))
        # Padding between metadata entries
        f.write('\n')


def logfunc(func):
    """ Logs a function's source code.
        
        Args:
            func (function): the function whose source code is to be logged.
    
        Returns:
            (None): none
    
    """
    log(_get_func_source(func))


######################## Plots ########################


def logfig():
    """ Logs the figure without showing it.
        
        Returns:
            (None): none
    
    """
    # If this is the first log being done.
    if SERIAL == None: gen_serial()
    
    plot_fname = PLOT_PATH / f'{SERIAL}.pdf'
    # Save the figure
    plt.savefig(plot_fname, bbox_inches='tight')    


def showfig():
    """ Wrapper to save figure to temp folder with current serial and show it.
    
        Returns:
            (None): none
    
    """
    # Log the figure, then show it.
    logfig()
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