#!/usr/bin/env bash
set -e

USE_APP_PATH=${APP_PATH:-/digi-srv}

cd ${USE_APP_PATH}
flask db upgrade
