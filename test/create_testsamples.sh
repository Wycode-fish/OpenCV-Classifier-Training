#!/bin/bash

opencv_createsamples -img ../positives/test_pic.jpg -num 100 -bg ../negatives.dat -info test.dat -maxxangle 0.6 -maxyangle 0 -maxzangle 0.3 -maxidev 100 -bgcolor 0 -bgthresh 0
