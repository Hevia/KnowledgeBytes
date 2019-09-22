from flask import Flask, render_template, request
import xml.dom.minidom as minidom
from flask_cors import CORS
import requests, json
import sys
import io
import summarize as anthony
import wikipedia_processing as komila
import wolfpack as aaron
from PIL import Image
import re
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

app = Flask(__name__)
CORS(app)
# CONSTANTS
animal = 'a'
person = 'h'
planet = 'p'
cities = 'c'

max_query_lengh = 100

with open("configs.json") as conf:
    config = json.load(conf)

wolfram_app_id = config["wolfram_id"] 
azure_cv_key = config["cv_id"] 
#print(azure_cv_key)

@app.route("/")
def main():
    return render_template("index.html")

def string_from_image(url_input):
    predictor = CustomVisionPredictionClient(azure_cv_key, endpoint="https://eastus.api.cognitive.microsoft.com/")

    image_response = requests.get(url_input, stream=True).raw
    image = Image.open(image_response)

    buf = io.BytesIO()
    image.save(buf, format='JPEG')
    image = buf.getvalue()

    #print(config["project_id"])
    results = predictor.classify_image(config["project_id"], "version0.2", image)

    top_predictions = results.predictions[0]
    return prediction.tag_name   

def categorize_string(s):

    url = aaron.build_request_url(s, ["Result"])
    #print(url)

    req = requests.get(url)
    #print(req.text)

    categories = {"Species" : animal, "Planet" : planet, "City" : 'c', "Person" : 'p'}

    dt = minidom.parseString(req.text)
    collection = dt.documentElement

    assumptions = collection.getElementsByTagName("assumptions")

    if not assumptions:
        return person

    assumption = assumptions[0].getElementsByTagName("assumption")[0]
    values = assumption.getElementsByTagName("value")

    for v in values:
        name = v.getAttribute("name")
        #print(name)
        if name in categories:
            return categories[name]

        if "::" in name:
            #print(name)
            return person

    return None

@app.route("/search_query", methods=["POST"])
def post_search_query():

    #input_string = request.json["query"]
    #input_string = "http://www.pets4homes.co.uk/images/breeds/10/large/c231b08a94097d24fb0577b5bcff1d74.jpg"
    input_string = "shark"

    # check if string is url
    if re.search("(?:http\:|https\:)?\/\/.*\.(?:png|jpg)", input_string):
        input_string = string_from_image(input_string)

    # validate input
    if not input_string or len(input_string) > max_query_lengh:
        return(json.encoder({"success" : False, "message" : "query length too long"}))

    # get category
    category = categorize_string(input_string)

    # get wiki data
    wiki_data = komila.create_maps(input_string)

    if category == animal:
        wolfram_data = aaron.process_animal(input_string)
        summary = anthony.summarize_animals(wiki_data, wolfram_data)

    elif category == person:
        wolfram_data = aaron.process_person(input_string)
        summary = anthony.summarize_person(wiki_data, wolfram_data)

    elif category == planet:
        wolfram_data = aaron.process_planet(input_string)
        summary = anthony.summarize_planets(wiki_data, wolfram_data)

    elif category == cities:
        wolfram_data = aaron.process_cities(input_string)
        summary = anthony.summarize_cities(wiki_data, wolfram_data)

    else:
        return json.encoder({"success" : False, "message" : "could not find category"})

    if not summary["success"]:
        return json.encoder({"success" : False, "message" : "failure in summarize"} )

    return summary

@app.route("/sample", methods=["POST"])
def get_sample_query():
    # For testing

    #{"query" : "user_search_term"}

    sample = request.json["query"]

    with open("scripts/data/mock_summary_zebra.json", 'r', encoding='UTF8') as f:
        sample = json.load(f.read())

    return sample

post_search_query()

if __name__ == "__main__":
    app.run()
