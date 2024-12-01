export FLASK_APP=vuln
export FLASK_DEBUG=true

pip3 install -r requirements.txt

flask db upgrade
flask run --host=0.0.0.0 --port=80
