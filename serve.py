"""Code for a flask API to Create, Read, Update, Delete users"""
import os

from journeys import create_app

# parser = argparse.ArgumentParser()
# parser.add_argument("--port", help="Port for debug server to listen on", default=4000)
# args = parser.parse_args()

debug = True
threaded = True
host = "127.0.0.1"
port = int(os.environ.get("PORT", 5000))
if os.environ.get("PORT"):
    host = "0.0.0.0"
    debug = False
    threaded = False

app = create_app()

app.run(debug=debug, threaded=threaded, host=host, port=port)
