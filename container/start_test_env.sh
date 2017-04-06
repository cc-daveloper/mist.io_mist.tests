#!/bin/sh
set -e

XVFB_WHD=${XVFB_WHD:-1280x720x16}

export DISPLAY=:1.0
export MIST_URL=${MIST_URL:-http://172.17.0.1}

# Start Xvfb
Xvfb :1 -ac -screen 0 $XVFB_WHD &

x11vnc -display :1.0 -listen 0.0.0.0 -rfbport 5900 &

cd /mist.core/src/mist.io/tests
pip install -e src/mist.io/tests

/bin/bash