#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn belt_exam.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3
