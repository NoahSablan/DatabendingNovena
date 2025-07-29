# Original code is from Audacity's mod-script-pipe, modified here to databend multiple tracks at once.
# This python script executes commands in Audacity to perform commands on raw image files as tracks.
# The script ensures the pipe connection and then sends commands to manipulate the audio data in the tracks.

import os
import sys
import time

# Set up pipe.
if sys.platform == 'win32':
    print("bulkDatabend.py, running on windows")
    TONAME = '\\\\.\\pipe\\ToSrvPipe'
    FROMNAME = '\\\\.\\pipe\\FromSrvPipe'
    EOL = '\r\n\0'
else:
    print("bulkDatabend.py, running on linux or mac")
    TONAME = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
    FROMNAME = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
    EOL = '\n'

# Check if the path exists to determine if mod-script-pipe is running properly.
# Sometimes, Audacity is running and it will still give this error for some reason.
# Sometimes, you need to run the script until it works.
print("Write to  \"" + TONAME +"\"")
if not os.path.exists(TONAME):
    print(" ..does not exist.  Ensure Audacity is running with mod-script-pipe.")
    sys.exit()

print("Read from \"" + FROMNAME +"\"")
if not os.path.exists(FROMNAME):
    print(" ..does not exist.  Ensure Audacity is running with mod-script-pipe.")
    sys.exit()

print("-- Both pipes exist.  Good.")

# Files need to be opened for writing and reading in order to get responses from Audacity.
TOFILE = open(TONAME, 'w')
print("-- File to write to has been opened")
FROMFILE = open(FROMNAME, 'rt')
print("-- File to read from has now been opened too\r\n")

# Sends a command to test connection to Audacity.
def send_command(command):
    """Send a single command."""
    print("Send: >>> \n"+command)
    TOFILE.write(command + EOL)
    TOFILE.flush()

# Gets response from audacity to determine if the command was successful.
def get_response():
    """Return the command response."""
    result = ''
    line = ''
    while True:
        result += line
        line = FROMFILE.readline()
        if line == '\n' and len(result) > 0:
            break
    return result

# Does a command first and prints out response from audacity.
def do_command(command):
    """Send one command, and return the response."""
    send_command(command)
    response = get_response()
    print("Rcvd: <<< \n" + response)
    return response

# This function executes Audacity commands. 
def databend_img():
    # Select track or tracks in the project in order to manipulate them.
    # In order to modify audio, the track must be selected.
    do_command('SelectAll:')

    # Start moving the playhead past the beginning of the track (the image file header).
    # Because we are dealing with image files, they contain headers that are not accounted for 
    # in audacity as audio data. 

    # If we do not move the playhead in audacity, it will manipulate the header, causing 
    # the output image file to be corrupted.
    do_command('PlayStopSelect:')

    # Sleep just one second, arbitrarily, to ensure the playhead has moved.
    time.sleep(1)

    # Stop playhead using PlayStopSelect, which stops playback and selects the track
    # starting from the current playhead position.
    do_command('PlayStopSelect:')


    # @TODO: parameterize the following command so that we can pass a preset
    # into this function to allow the script to do different databends.
    
    # The following are exmples of commands that can be used to manipulate the audio.
    #   Amplify audio:
    # do_command('Amplify:Ratio=0.7')
    #   Bass and Treble adjustment:
    # do_command('BassAndTreble:Bass=0.5 Treble=-0.5')
    
    # Do the databend.
    do_command('ChangeTempo: Percentage=3')

    
    # @TODO: When audacity supports direct exporting to raw audio files,
    # we can export the raw audio file here.
    # do_command('Export2:Filename="./testModRaw.raw"')

databend_img()