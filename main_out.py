import cv2
from utils.align_custom import AlignCustom
from utils.face_feature import FaceFeature
from utils.mtcnn_detect import MTCNNDetect
from utils.tf_graph import FaceRecGraph
import argparse
import sys
import json
import numpy as np
import time
import os, sys
import subprocess
count=0

def main():
    camera_recog()
  
def camera_recog():
    #subprocess.call(['/home/shunya/Desktop/FaceRec/gpio.sh'])
    count=0
    recog_data=[('', 0)]
    print("[INFO] camera sensor warming up...")
    vs = cv2.VideoCapture(0); #get input from webcam
    while True:
        _,frame = vs.read();
        #u can certainly add a roi here but for the sake of a demo i'll just leave it as simple as this
        rects, landmarks = face_detect.detect_face(frame,80);#min face size is set to 80x80
        aligns = []
        positions = []
        #print(rects)
        for (i, rect) in enumerate(rects):
            aligned_face, face_pos = aligner.align(160,frame,landmarks[i])
            if len(aligned_face) == 160 and len(aligned_face[0]) == 160:
                aligns.append(aligned_face)
                positions.append(face_pos)
            else: 
                print("Align face failed") #log 
            prev_recog = recog_data[0][0]       
            if(len(aligns) == 1 and face_pos=='Center') :
                # print(len(aligns))
                features_arr = extract_feature.get_features(aligns)
                recog_data = findPeople(features_arr,positions);
                cv2.rectangle(frame,(rect[0],rect[1]),(rect[0] + rect[2],rect[1]+rect[3]),(255,0,0))
                cv2.putText(frame,recog_data[0][0]+" - "+str(recog_data[0][1])+"%",(rect[0],rect[1]),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1,cv2.LINE_AA)
                per = recog_data[0][0]
                #time.sleep(0.1)
                print("Current",recog_data)
                print("Previous",prev_recog)

                if(per[0]=='l'):
                    if(per != prev_recog):
                        count=0
                    count=count+1
                    print("................................>",count)
                    if (count==7):
                        print("Final Label:$$$$$$$$$$$$$$$$$$$$$$$$$$",per)
                        subprocess.call(['./utils/ladoo.sh'])
                        count=0
                        time.sleep(0.3)
                        subprocess.call(['./utils/zero.sh'])

                if(per[0]=='m'):
                    if(per != prev_recog):
                        count=0
                    count=count+1
                    print("................................>",count)
                    if (count==7):
                        print("Final Label:$$$$$$$$$$$$$$$$$$$$$$$$$",per)
                        subprocess.call(['./utils/modak.sh'])
                        count=0
                        time.sleep(0.3)
                        subprocess.call(['./utils/zero.sh'])

                if(per[0]=='p'):
                    if(per != prev_recog):
                        count=0
                    count=count+1
                    print("................................>",count)
                    if (count==10):
                        print("Final Label:$$$$$$$$$$$$$$$$$$$$$$$$$$",per)
                        subprocess.call(['./utils/pedha.sh'])
                        count=0
                        time.sleep(0.3)
                        subprocess.call(['./utils/zero.sh'])			
 
        cv2.imshow("Frame",frame)
        #print(recog_data[0][0])
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

def findPeople(features_arr, positions, thres = 0.85, percent_thres = 85):

    f = open('./facerec_new.txt','r')
    data_set = json.loads(f.read());
    returnRes = [];
    for (i,features_128D) in enumerate(features_arr):
        result = "Unknown";
        smallest = sys.maxsize
        for person in data_set.keys():
            person_data = data_set[person][positions[0]];
            for data in person_data:
                distance = np.sqrt(np.sum(np.square(data-features_128D)))
                if(distance < smallest):
                    smallest = distance;
                    result = person;
        percentage =  min(100, 100 * thres / smallest)
        if percentage <= percent_thres :
            result = "Unknown"
        returnRes.append((result,percentage))
        #print(result)
    return returnRes



if __name__ == '__main__':
    FRGraph = FaceRecGraph();
    aligner = AlignCustom();
    extract_feature = FaceFeature(FRGraph)
    face_detect = MTCNNDetect(FRGraph, scale_factor=2); #scale_factor, rescales image for faster detection
    main();
