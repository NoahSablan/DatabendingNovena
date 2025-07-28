# Original code from Audacity's mod-script-pipe.
# This python script executes commands in Audacity to perform commands on raw image files as tracks.
# The script ensures the pipe connection and then sends commands to manipulate the audio data in the tracks.

import os
import sys
import time

# Set up pipe
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

print("Write to  \"" + TONAME +"\"")
if not os.path.exists(TONAME):
    print(" ..does not exist.  Ensure Audacity is running with mod-script-pipe.")
    sys.exit()

print("Read from \"" + FROMNAME +"\"")
if not os.path.exists(FROMNAME):
    print(" ..does not exist.  Ensure Audacity is running with mod-script-pipe.")
    sys.exit()

print("-- Both pipes exist.  Good.")

# Open
TOFILE = open(TONAME, 'w')
print("-- File to write to has been opened")
FROMFILE = open(FROMNAME, 'rt')
print("-- File to read from has now been opened too\r\n")

# Test Send
def send_command(command):
    """Send a single command."""
    print("Send: >>> \n"+command)
    TOFILE.write(command + EOL)
    TOFILE.flush()

# Test Response
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

def do_command(command):
    """Send one command, and return the response."""
    send_command(command)
    response = get_response()
    print("Rcvd: <<< \n" + response)
    return response

# This function executes Audacity commands. 
def databend_img():
    # Select track in project.
    do_command('SelectAll:')

    # Start moving the playhead past the beginning of the track (the image file header).
    do_command('PlayStopSelect:')

    # Let audio play to avoid manipulating header.
    time.sleep(1)
    do_command('PlayStopSelect:')

    # Do the databend.
    # TODO: parameterize the following command so that we can pass a preset
    # into this function to allow the script to do different databends.
    
    # The following are exmples of commands that can be used to manipulate the audio.
    # Amplify audio:
    # do_command('Amplify:Ratio=0.7')

    # Bass and Treble adjustment:
    # do_command('BassAndTreble:Bass=0.5 Treble=-0.5')
    
    do_command('ChangeTempo: Percentage=3')
    # TODO: When audacity supports direct exporting to raw audio files,
    # we can export the raw audio file here.
    # do_command('Export2:Filename="./testModRaw.raw"')

databend_img()