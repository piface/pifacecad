### BEGIN INIT INFO
# Provides: pifacecadsysinfo
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start pifacecad status daemon at boot time.
# Description:       Start pifacecad status daemon at boot time.
### END INIT INFO

LOCKFILE="/var/lock/pifacecad_status_service.lock"
SYSINFO_FILE="/usr/share/doc/python3-pifacecad/examples/sysinfo.py"

start() {
        echo -n "Starting PiFace CAD status service: "
        /usr/bin/python3 $SYSINFO_FILE &
        ### Create the lock file ###
        echo $! > $LOCKFILE
        status
}

stop() {
        echo -n "Stopping PiFace CAD status service: "
        pid=$(cat $LOCKFILE)
        kill $pid
        # Now, delete the lock file ###
        rm -f $LOCKFILE
        # clean up the screen
        /usr/bin/python3 $SYSINFO_FILE clear &
        status
}

status() {
        if [ -e $LOCKFILE ]
        then
            echo "[Running]"
        else
            echo "[Stopped]"
        fi
}

### main logic ###
case "$1" in
  start)
        start
        ;;
  stop)
        stop
        ;;
  status)
        status
        ;;
  restart|reload|force-reload)
        stop
        start
        ;;
  *)
        echo $"Usage: $0 {start|stop|restart|reload|force-reload|status}"
        exit 1
esac
exit 0
