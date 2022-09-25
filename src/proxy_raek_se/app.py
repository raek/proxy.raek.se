from flask import Flask, Response
from .client import fetch_bytes


app = Flask(__name__)


@app.route("/gemini/<path:url_without_scheme>")
def gemini(url_without_scheme):
    with fetch_bytes("gemini://" + url_without_scheme) as (mime_type, f):
        return f.read(), 200, {"Content-Type": mime_type}
