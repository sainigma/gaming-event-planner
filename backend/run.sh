cd "$(dirname "$(realpath "$0")")"
VENVDIR=./venv

if [ -d "$VENVDIR" ]; then
 source ./venv/bin/activate
else
 python3 -m venv venv
 source ./venv/bin/activate
 pip3 install flask
fi
flask run
deactivate