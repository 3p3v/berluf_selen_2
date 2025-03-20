#!/bin/sh
BASEDIR=$(dirname "$0")

# run virtual serial sockets
socat -d -d pty,link=/srv/pts/ttyV0,raw pty,link=/srv/pts/ttyV1,raw &

# run recuperator test script
python "$BASEDIR/recup.py" &

# run hass
bash scripts/develop

# wait for user to kill th script
sleep infinity &
wait

