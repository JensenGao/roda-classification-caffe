#!/usr/bin/env sh
# Compute the mean image from the imagenet training lmdb
# N.B. this is available in data/ilsvrc12

EXAMPLE=/home/jensengao/Desktop/roadProcessedData/TrainModel
DATA=/home/jensengao/Desktop/roadProcessedData/TrainModel
TOOLS=/home/jensengao/Downloads/caffe-master/.build_release/tools

$TOOLS/compute_image_mean $EXAMPLE/train_lmdb \
  $DATA/imagenet_mean.binaryproto

echo "Done."
