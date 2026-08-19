from website import create_site
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


if __name__ == "__main__":
    args = parser.parse_args()
    if args.development:
        app = create_site(config="development")
    else:
        app = create_site(config="production")
    app.run()
