#!/bin/bash
killall python
./manage.py runfcgi method=threaded daemonize=true host=127.0.0.1 port=3033
