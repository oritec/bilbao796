#! /bin/sh
# /etc/init.d/mqttConsumer

### BEGIN INIT INFO
# Provides:          mqttConsumer
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Simple script to start a program at boot
# Description:       A simple script from www.stuffaboutcode.com which will start / stop a program a boot / shutdown.
### END INIT INFO

# If you want a command to always run, put it here

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting mqttConsumer"
    # run application you want to start
    /usr/bin/python /home/pi/bilbao796/trunk/mqttConsumer.py >/tmp/script_stdout.txt 2>&1 &
    ;;
  stop)
    echo "Stopping noip"
    # kill application you want to stop
    pkill -f mqttConsumer.py
    ;;
  *)
    echo "Usage: /etc/init.d/mqttConsumer {start|stop}"
    exit 1
    ;;
esac

exit 0 