#!/usr/bin/env python

'''
Multithreaded video processing sample.
Usage:
   video_threaded.py {<video device number>|<video file name>}

   Shows how python threading capabilities can be used
   to organize parallel captured frame processing pipeline
   for smoother playback.

Keyboard shortcuts:

   ESC - exit
   space - switch between multi and single threaded processing
'''


import numpy as np
import cv2

from multiprocessing.pool import ThreadPool
from collections import deque

from common import clock, draw_str, StatValue
import video


class DummyTask:
    def __init__(self, data):
        self.data = data
    def ready(self):
        return True
    def get(self):
        return self.data

if __name__ == '__main__':
    import sys

    print __doc__

    try: fn = sys.argv[1]
    except: fn = 0
    cap = cv2.VideoCapture(fn)
    print cap


    def process_frame(frame, t0):
        # some intensive computation...
        #frame = cv2.equalizeHist(frame)
        return frame, t0

    threadn = cv2.getNumberOfCPUs()
    pool = ThreadPool(processes = threadn)
    pending = deque()

    threaded_mode = True

    latency = StatValue()
    frame_interval = StatValue()
    last_frame_time = clock()
    
    while True:
        while len(pending) > 0 and pending[0].ready():
            res, t0 = pending.popleft().get()
            latency.update(clock() - t0)
            draw_str(res, (20, 20), "threaded      :  " + str(threaded_mode))
            draw_str(res, (20, 40), "latency        :  %.1f ms" % (latency.value*1000))
            draw_str(res, (20, 60), "frame interval :  %.1f ms" % (frame_interval.value*1000))
            cv2.imshow('threaded video', res)
        if len(pending) < threadn:
            ret, frame = cap.read()
            if ret :
                print frame.shape
            else:
                break
            t = clock()
            frame_interval.update(t - last_frame_time)
            last_frame_time = t
            task = pool.apply_async(process_frame, (frame.copy(), t))
            pending.append(task)
        
        ch = 0xFF & cv2.waitKey(1)

        if ch == 27:
            break
cv2.destroyAllWindows()
