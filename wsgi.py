from website import create_site

"""
    This file is used by Gunicorn to bind to the Flask app.
    For local running use run.py where debug mode can be easily set.
"""

app = create_site(config="production")

if __name__ == "__main__":
    app.run()
