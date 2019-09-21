from flask import Flask, render_template, request
import requests, json

app = Flask(__name__)

with open("local/app_id") as f:
    wolfram_app_id = f.read().strip()

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/search_query", methods=["POST"])
def post_search_query(input_string):
    return None

@app.route("/sample", methods=["POST"])
def get_sample_query():
    # For testing

    #{"query" : "user_search_term"}

    sample = request.json["query"]
    return json.dumps(sample)

if __name__ == "__main__":
    app.run()