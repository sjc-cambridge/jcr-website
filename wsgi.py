from website import create_site
import os

curr_dir = os.path.dirname(__file__)
instancepath = os.path.join(curr_dir, 'instance')
if not os.path.exists(instancepath):
    """Create instance folder as reminder to make config.py inside"""
    os.makedirs(instancepath)

app = create_site()

if __name__ == "__main__":
    app.run()
