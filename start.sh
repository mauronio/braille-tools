#!/bin/sh
. ./env/bin/activate
cd application
nohup ./run.sh > server.out 2>&1 &
