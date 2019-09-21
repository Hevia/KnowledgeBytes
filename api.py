from flask import Flask, render_template, request
import requests, json

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/search_query", methods=["POST"])
def post_search_query(input_string):
    return None

@app.route("/sample")
def get_sample_query(input_string="cats"):
    # For testing
    return None


if __name__ == "__main__":
    app.run()
    