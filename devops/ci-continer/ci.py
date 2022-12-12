from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Render index.html
@app.post("/triger")
def staff_are_pushed():
    os.system("bash start_testing.sh")
    return "running script to pull the data... test will be sent by mail"

# Render index.html
@app.get("/")
def home_page():
    return render_template("index.html")

# Render index.html
@app.get("/health")
def health_check():
    return "OK"


if __name__ == '__main__':
    app.run(host="0.0.0.0")
