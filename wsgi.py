from website import create_site
import os

"""
    This file is used by Gunicorn to bind to the Flask app.
    For local running use run.py where debug mode can be easily set.
"""

curr_dir = os.path.dirname(__file__)
instancepath = os.path.join(curr_dir, 'instance')
if not os.path.exists(instancepath):
    """Create instance folder as reminder to make config.py inside"""
    os.makedirs(instancepath)

app = create_site(config='production')

if __name__ == "__main__":
    app.run()
