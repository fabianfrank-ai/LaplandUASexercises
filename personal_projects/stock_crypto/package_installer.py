import subprocess
import sys

packages = [
    'streamlit',
    'pandas',
    'yfinance',
    'matplotlib',
    'sqlite3',
    'urllib',
    'subprocess',
    'sys'
]

def install(packages):
    for p in packages:
        try:
            __import__(p)
        except ImportError:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', p]) 
