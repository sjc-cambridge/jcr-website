## Project Structure
The files production.py and development.py can be used to differentiate between
running in production and development, you could also have different config
set-ups, see args of 'create_site' function.

Currently the config files don't do much but could in future be used to
distinguish between development and production databases and more complex things.

Any secure keys should be stored in .env, see .env.example (see handover)
