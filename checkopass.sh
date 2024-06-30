#!/bin/bash

APP_PATH=./
LOGS_PATH=./logs
PID_PATH=./pid
BACKEND_URL=http://localhost:5000

start_apps() {
    mkdir -p $LOGS_PATH
    mkdir -p $PID_PATH

    echo "[INFO] Starting backend application"
    nohup python $APP_PATH/backend.py > $LOGS_PATH/backend.log 2>&1 &
    echo $! > $PID_PATH/backend_pid.txt
    echo -n "[DEBUG] PID of backend app: " && cat $PID_PATH/backend_pid.txt

    echo -n "[INFO] Waiting for backend to be available"
    while ! curl -s $BACKEND_URL > /dev/null; do
        echo -n "."
        sleep 1
    done
    
    echo
    echo "[INFO] Backend is up! Starting frontend application"

    nohup python $APP_PATH/frontend.py > $LOGS_PATH/frontend.log 2>&1 &
    echo $! > $PID_PATH/frontend_pid.txt
    echo -n "[DEBUG] PID of frontend app: " && cat $PID_PATH/frontend_pid.txt

    echo "[INFO] Applications are running in the background"
}

stop_apps() {
    if [ -f "$PID_PATH/backend_pid.txt" ]; then
        BACKEND_PID=$(cat $PID_PATH/backend_pid.txt)
        echo "[INFO] Stopping backend application with PID $BACKEND_PID"
        kill $BACKEND_PID
        rm $PID_PATH/backend_pid.txt
        echo "[INFO] Backend application is stopped"
    else
        echo "[ERROR] Backend PID file not found. Is the backend running?"
    fi

    if [ -f "$PID_PATH/frontend_pid.txt" ]; then
        FRONTEND_PID=$(cat $PID_PATH/frontend_pid.txt)
        echo "[INFO] Stopping frontend application with PID $FRONTEND_PID"
        kill $FRONTEND_PID
        rm $PID_PATH/frontend_pid.txt
        echo "[INFO] Frontend application is stopped"
    else
        echo "[ERROR] Frontend PID file not found. Is the frontend running?"
    fi
}

case $1 in
    start)
        start_apps
        ;;
    stop)
        stop_apps
        ;;
    restart)
        stop_apps
        start_apps
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac
