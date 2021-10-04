#!/bin/sh
export LC_ALL=en_US.utf-8
export LANG=en_US.utf-8
export FLASK_APP=web_controller.py
flask run --host=0.0.0.0 --port=8080

