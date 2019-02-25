#!/usr/bin/python3

# wapi flask interface start point

import optparse
import app
import traceback


#app = Flask(__name__)
#app.config.from_envvar('YOURAPPLICATION_SETTINGS')

def parse_args():
    usage = """
    python3 wapi.py --server
"""
    parser = optparse.OptionParser(usage)

    help = "Start Flask server"
    parser.add_option('--start-server', action="store_true", dest="server", help=help, default=False)

    help = "Set path to Flask config"
    parser.add_option('--fc', type=str, dest="flask_config", help=help, default="./config/flask.cfg")

    options, args = parser.parse_args()

    return options

def main():
    options = parse_args()
    try:
    	if options.server == True:
            flask_server = app.router.Wapi(fc=options.flask_config)
    except Exception as e:
        print("Wapi Main loop Exception")
        traceback.print_exc()

if __name__ == '__main__':
    main()