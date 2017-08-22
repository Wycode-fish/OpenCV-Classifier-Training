#!/bin/bash

#opencv_haartraining  -data haarcascade -vec samples.vec -bg negatives.dat -nstages 20 -nsplits 2 -minhitrate 0.999 -maxfalsealarm 0.5 -npos 310 -nneg 600 -w 20 -h 20 -nonsym -mem 1024 -mode ALL

opencv_traincascade  -data haarcascade -vec samples.vec -bg negatives.dat -numStages 20 -minHitRate 0.999 -maxFalseAlarmRate 0.5 -numPos 600 -numNeg 800 -w 20 -h 20 -mode ALL
