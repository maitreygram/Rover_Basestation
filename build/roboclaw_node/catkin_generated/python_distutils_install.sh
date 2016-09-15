#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
    DESTDIR_ARG="--root=$DESTDIR"
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/utkarsh/rover_ws/src/roboclaw_node"

# snsure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/utkarsh/rover_ws/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/utkarsh/rover_ws/install/lib/python2.7/dist-packages:/home/utkarsh/rover_ws/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/utkarsh/rover_ws/build" \
    "/usr/bin/python" \
    "/home/utkarsh/rover_ws/src/roboclaw_node/setup.py" \
    build --build-base "/home/utkarsh/rover_ws/build/roboclaw_node" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/home/utkarsh/rover_ws/install" --install-scripts="/home/utkarsh/rover_ws/install/bin"
