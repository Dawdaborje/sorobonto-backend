#!/usr/bin/bash
source venv/bin/activate

cd sorobonto

DEBUG=FALSE python3.12 manage.py runserver