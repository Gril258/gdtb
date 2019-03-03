#!/usr/bin/python3

# wapi flask interface start point

import optparse
import traceback
import app


def parse_args():
    usage = """
    python3 wapi.py --start-server
"""
    parser = optparse.OptionParser(usage)

    help = "Start Flask server"
    parser.add_option('--start-server', action="store_true", dest="server", help=help, default=False)

    help = "Start Flask server"
    parser.add_option('--start-reactor', action="store_true", dest="reactor", help=help, default=False)

    options, args = parser.parse_args()

    return options

def main():
    options = parse_args()

    if options.reactor == True and options.server == True:
        print("Cannot start both server and reactor with this command, choose --start-server OR --start-reactor")
        exit(1)
    
    try:
        if options.server == True:
            app.router.Wapi()
        elif options.reactor == True:
            app.reactor.instance()
        	
    except Exception:
        print("Wapi Main loop Exception")
        traceback.print_exc()

if __name__ == '__main__':
    main()