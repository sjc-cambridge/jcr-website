"""
Setting to debug mode only works if you run the app with 'python3 run.py -d'
File has little use at the moment but could in future be used to distuingish
between development and production databases etc.
Secure keys should be stored in .env, see .env.example (see handover)
"""

ENV = "production"
DEBUG = False
