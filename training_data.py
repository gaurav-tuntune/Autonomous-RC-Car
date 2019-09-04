import numpy as np
from grabscreen import grab_screen
import cv2
import time
from getkeys import key_check
import os
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,
	help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
	help="Whether or not frames should be displayed")
args = vars(ap.parse_args())


def keys_to_output(keys):
    '''
    Convert keys to a ...multi-hot... array
    [A,W,D] boolean values.
    '''
    output = [0,0,0]
    
    if 'LEFT' in keys:
        output[0] = 1
    elif 'DOWN' in keys:
        output[2] = 1
    elif 'UP' in keys:
        output[1] = 1
    return output


file_name = 'training_data(1).npy'

if os.path.isfile(file_name):
    print('File exists, loading previous data!')
    training_data = list(np.load(file_name))
else:
    print('File does not exist, starting fresh!')
    training_data = []


def main():

    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)


    paused = False
    while(True):

        if not paused:
            # 800x600 windowed mode
            #screen = grab_screen(region=(0,40,800,640))
            last_time = time.time()
            vs = WebcamVideoStream(src=0).start()
            fps = FPS().start()
 
            # loop over some frames...this time using the threaded stream
            while fps._numFrames < args["num_frames"]:
                # grab the frame from the threaded video stream and resize it
                # to have a maximum width of 400 pixels
                frame = vs.read()
                screen = imutils.resize(frame, width=400)
                screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
                final = cv2.resize(screen, (80,60))
                #cv2.imshow("Frame", screen)
                #cv2.imshow("Frame2", final)
            # resize to something a bit more acceptable for a CNN
            keys = key_check()
            output = keys_to_output(keys)
            training_data.append([screen,output])
            
            if len(training_data) % 5000 == 0:
                print(len(training_data))
                np.save(file_name,training_data)

        keys = key_check()
        if 'T' in keys:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)


main()
