#!/bin/bash

gunicorn "app:create_app()" -w 2 --threads 2 -b 0.0.0.0:443 --log-level debug --keyfile=key.pem --certfile=cert.pem --access-logfile access.log
