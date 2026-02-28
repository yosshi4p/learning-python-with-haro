from flask import Flask, request

app = Flask(__name__)

@app.get("/")
def home():
    name = request.args.get("name", "よっちん")
    return f"Hello, {name}! (Flask on Sakura Shared)"