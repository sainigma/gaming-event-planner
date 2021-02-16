#!/bin/bash
# Run with parameter -new if you want to reinitialize the whole system

VENVDIR=./venv
OGDIR="$PWD"
WORKDIR="$(dirname "$(realpath "$0")")"

function _new () {
  if [ "$1" == "-new" ]; then
    echo "poistan"
    rm -rf ./venv
  fi
}

function _init {
  python3 -m venv venv
  source ./venv/bin/activate
  pip3 install flask
  pip3 install python-dotenv
  pip3 install igdb-api-v4
  pip3 install requests
  pip3 install pyjwt
  pip3 install gunicorn
  pip3 freeze > ./../requirements.txt
  deactivate
}

function _clean {
  rm ./dummy.db
  rm ./../dummy.db
}

function _start {
  if [ -d "$VENVDIR" ]; then
    source ./venv/bin/activate
    clear
    flask run
    deactivate
#    _clean
  else
    _init
    _start
  fi
}

cd "$WORKDIR"
_new "$1"
_start
cd "$OGDIR"