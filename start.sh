#!/bin/sh
. ./env/bin/activate
pip install -r requirements.txt
cd application
nohup ./run.sh > server.out 2>&1 &
