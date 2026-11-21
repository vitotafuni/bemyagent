#!/bin/sh
# runs the arms given as args "arm model prompt" lines on stdin, 3 at a time
xargs -P3 -L1 "$(dirname "$0")/run-arm.sh"
