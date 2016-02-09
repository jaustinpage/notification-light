#!/usr/bin/env python

from fnmatch import fnmatch
import logging
import os
import subprocess
import time
import traceback
import sys

logging.basicConfig(filename='logs/notification-light.log', level=logging.DEBUG)

def find_cameras():
    '''
    Gets all of the devices that include the word 'video' in it
    '''
    for f in os.listdir('/dev'):
        if fnmatch(f, 'video*'):
            video_camera_path = os.path.join('/dev', f)
            logging.debug('Found video camera %s' % video_camera_path)
            yield video_camera_path

def cameras_in_use(cameralist):
    '''
    Returns an iterator that yeilds all of the processes that have the file open
    '''
    for camera in cameralist:
        try:
            if subprocess.check_output(['/usr/bin/lsof', '-w', '-Fp', camera]):
                return True
        except subprocess.CalledProcessError as err:
            return False
            # Not sure why this returns -1 on none found, but, it does...
            #stacktrace = traceback.format_exc(sys.exc_info())
            #logging.debug('Exception calling /usr/bin/lsof. Stacktrace:\n%s' % stacktrace)

def light_red():
    try:
        subprocess.check_output(['/home/aust9600/github/notification-light/blink1/commandline/blink1-tool', '--red'])
    except subprocess.CalledProcessError as err:
        stacktrace = traceback.format_exc(sys.exc_info())
        logging.debug('Exception in light_red() calling blink1-tool. Stacktrace:\n%s' % stacktrace)

def light_off():
    try:
        subprocess.check_output(['/home/aust9600/github/notification-light/blink1/commandline/blink1-tool', '--off'])
    except subprocess.CalledProcessError as err:
        stacktrace = traceback.format_exc(sys.exc_info())
        logging.debug('Exception in light_off() calling blink1-tool. Stacktrace:\n%s' % stacktrace)

def main():
    '''
    This is the main function yo. Sets up and handles the loop
    '''
    logging.debug('Notification light was started')
    while True:
        if cameras_in_use(list(find_cameras())):
            light_red()
        else:
            light_off()
        time.sleep(6)

if __name__ == '__main__':
    '''
    The default thing to do.
    '''
    main()
