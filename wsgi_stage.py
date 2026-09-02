"""Wrapper WSGI minimo per servire AutoTrack (sito statico) sullo slot
gunicorn condiviso di stage.ideadibusiness.com (porta 8081), che si
aspetta un modulo app:app come le altre app Flask gestite da set_stage.sh.
"""
import os

from flask import Flask, send_from_directory

ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)


@app.route('/')
@app.route('/<path:path>')
def serve(path='index.html'):
    return send_from_directory(ROOT, path)
