import argparse
from . import APRS
import sys


def main() -> int:

    # Set up argument parsing
    ap = argparse.ArgumentParser()
    ap.add_argument("api_key", help="APRS.fi API key")
    ap.add_argument("callsign", help="Callsign to query")
    ap.add_argument("-t", "--type", help="Query type",
                    choices=["loc", "wx", "msg"], default="loc")
    args = ap.parse_args()

    # Make API connection
    api = APRS(args.api_key)

    # Make call
    output = []
    if args.type == "loc":
        output = list(api.getLocation(args.callsign))
    elif args.type == "msg":
        output = list(api.getMessages(args.callsign))

    if not len(output):
        print("No data")
        return 0

    # Dump the output
    for entry in output:
        print(":::: New Entry ::::")
        for var in vars(entry):
            print(f"{var.capitalize()}: {entry.__dict__[var]}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
