export FLASK_APP=app
export FLASK_DEBUG=true

pip3 install -r requirements.txt

flask run --cert=adhoc --host=0.0.0.0 --port=443
