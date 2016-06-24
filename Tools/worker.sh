#!/usr/bin/env bash
source /home/sistemas/.Fastwork/bin/activate
celery -A Fastwork worker -l info -B