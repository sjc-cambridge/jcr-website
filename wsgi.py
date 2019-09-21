from website import create_site
from dotenv import load_dotenv
from pathlib import Path  # python3 only
import os

app = create_site()

if __name__ == "__main__":
    print('hello')
    app.run()
