#!/bin/bash
set +x
celery -A application  worker -B --loglevel=debug
