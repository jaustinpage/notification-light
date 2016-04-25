#!/usr/bin/env python

import daemon
from fnmatch import fnmatch
import inotify.adapters
import logging
import os
import subprocess
import time
import traceback
import sys


_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
_LOGGER = logging.getLogger(__name__)

def _configure_logging(log_level=logging.WARNING):
     '''
     Set up some common logging stuff. Source this from module functions or class functions
     '''
     _LOGGER.setLevel(log_level)
 
     ch = logging.StreamHandler()
     formatter = logging.Formatter(_LOG_FORMAT)
     ch.setFormatter(formatter)
 
     _LOGGER.addHandler(ch)
     _LOGGER.info("Logger configured")


def light_red():
    try:
        subprocess.check_output(['/home/jaustinpage/github/blink1/commandline/blink1-tool', '--red'])
    except subprocess.CalledProcessError as err:
        stacktrace = traceback.format_exc(sys.exc_info())
        logging.debug('Exception in light_red() calling blink1-tool. Stacktrace:\n%s' % stacktrace)


def light_off():
    try:
        subprocess.check_output(['/home/jaustinpage/github/blink1/commandline/blink1-tool', '--off'])
    except subprocess.CalledProcessError as err:
        stacktrace = traceback.format_exc(sys.exc_info())
        logging.debug('Exception in light_off() calling blink1-tool. Stacktrace:\n%s' % stacktrace)


class CameraMonitor(object):
    '''
    This is a class that monitors a camera
    '''
    def __init__(self, camera_path):
        super(CameraMonitor, self).__init__()
        self.camera_path = camera_path

    def watch(self):
        '''
        This watches a camera, and reacts when it is changed
        '''
        self.i = inotify.adapters.Inotify()
        self.i.add_watch(self.camera_path)
        try:
            for event in self.i.event_gen():
                if event is not None:
                    (header, type_names, watch_path, filename) = event
                    _LOGGER.debug("WD=(%d) MASK=(%d) COOKIE=(%d) LEN=(%d) MASK->NAMES=%s "
                                 "WATCH-PATH=[%s] FILENAME=[%s]",
                                  header.wd, header.mask, header.cookie, header.len, type_names,
                                  watch_path, filename)
                    if header.mask == 32:
                        light_red()
                    if header.mask == 8:
                        light_off()
        finally:
            self.i.remove_watch(self.camera_path)


#def find_cameras():
#    '''
#    Gets all of the devices that include the word 'video' in it
#    '''
#    for f in os.listdir('/dev'):
#        if fnmatch(f, 'video*'):
#            video_camera_path = os.path.join('/dev', f)
#            logging.debug('Found video camera %s' % video_camera_path)
#            yield video_camera_path


def _main():
    '''
    This is the main function yo. Sets up and handles the loop
    '''
    _configure_logging(logging.DEBUG)
    _LOGGER.debug('Notification light was started')
    camera_path = '/dev/video1'
    camera = CameraMonitor(camera_path)
    camera.watch()

if __name__ == '__main__':
    '''
    The default thing to do.
    '''
    with daemon.DaemonContext():
        _main()
