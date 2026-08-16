from website import create_site
import os
from argparse import ArgumentParser


"""
    File used for running Flask app locally.
    Run in development mode with 'python3 run.py -d'
"""

parser = ArgumentParser()
parser.add_argument(
    "-d",
    "--development",
    action="store_true",
    help="Run app with development config",
)


curr_dir = os.path.dirname(__file__)
instancepath = os.path.join(curr_dir, "instance")
if not os.path.exists(instancepath):
    """Create instance folder as reminder to make config.py inside"""
    os.makedirs(instancepath)

if __name__ == "__main__":
    args = parser.parse_args()
    if args.development:
        app = create_site(config="development")
    else:
        app = create_site(config="production")
    app.run()
