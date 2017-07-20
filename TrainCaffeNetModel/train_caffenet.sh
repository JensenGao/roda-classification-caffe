#!/usr/bin/env sh
set -e

/home/jensengao/Downloads/caffe-master/.build_release/tools/caffe train \
    --solver=/home/jensengao/Desktop/MyProject/TrainModel/Model/solver.prototxt $@
