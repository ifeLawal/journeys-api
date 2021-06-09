"""Code for a flask API to Create, Read, Update, Delete users"""
import argparse

from journeys import create_app

parser = argparse.ArgumentParser()
parser.add_argument("--port", help="Port for debug server to listen on", default=4000)
args = parser.parse_args()

app = create_app()

app.run(debug=True, threaded=True, host="127.0.0.1", port=args.port)
