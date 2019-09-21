from flask import Flask, render_template, request
import xml.dom.minidom as minidom
import requests, json

app = Flask(__name__)

# CONSTANTS
animal = 'a'
history = 'h'

max_query_lengh = 100

#with open("local/app_id") as f:
#    wolfram_app_id = f.read().strip()

@app.route("/")
def main():
    return render_template("index.html")

def categorize_string(s):
    # TODO
    return animal

def process_animal(input_string, options=["ScientificName:SpeciesData", "Taxonomy:SpeciesData", "SpeciesDataPhysicalProperties"]):

    # get api key
    #with open("local/app_id") as f:
    #olfram_app_id = f.read().strip()

    # build request url
    url = "http://api.wolframalpha.com/v2/query?appid=" + wolfram_app_id
    url += "&input=" + input_string
    url += "&format=plaintext"

    for o in options:
        url += "&includepodid=" + o

    print(url)
    # do request
    req = requests.get(url)

    # Initialize xml parsing tools -- this turns the xml file into a tree that we can work with
    dt = minidom.parseString(req.text)
    collection = dt.documentElement
    pods = collection.getElementsByTagName("pod")

    scientific_name = ""
    taxonomy = ""
    biological_properties = {}

    for pod in pods:
        #print("hi")

        # get scientific name
        if str(pod.getAttribute("title")) == "Scientific name":
            temp = pod.getElementsByTagName("subpod")[0]
            scientific_name = temp.getElementsByTagName("plaintext")[0].firstChild.nodeValue

            continue

        # Get Biological Properties
        if str(pod.getAttribute("title")) == "Biological properties":

            for sub in pod.getElementsByTagName("subpod"):
                print(sub.getAttribute("title"))
                propstring = sub.getElementsByTagName("plaintext")[0].firstChild.nodeValue
                #print(propstring)

                i = 0
                ps = propstring.replace('\n', '|').split('|')
                print(ps)

                while i < len(ps) - 1:
                    biological_properties[ps[i].strip()] = ps[i+1].strip()
                    i += 2

            continue

        if str(pod.getAttribute("title")) == "Taxonomy":
            temp = pod.getElementsByTagName("subpod")[0]

            i = 0
            taxstring = temp.getElementsByTagName("plaintext")[0].firstChild.nodeValue

            ts = taxstring.replace('\n', '|').split('|')
            taxonomy = []

            for t in ts:

                if i == 1:
                    taxonomy.append(t)

                i = (i+1) % 2

    return json.dumps({"scientific name" : scientific_name, "Taxonomy" : taxonomy, "biological properties" : biological_properties})

@app.route("/search_query", methods=["POST"])
def post_search_query():

    input_text = request.json["query"]

    # validate input
    if len(input_string) > max_query_lengh:
        return(json.encoder({"success" : "false", "message" : "query length too long"}))

    # get category
    category = categorize_string(input_text)

    if category == animal:
        process_animal(input_string)

    return None

@app.route("/sample", methods=["POST"])
def get_sample_query():
    # For testing

    #{"query" : "user_search_term"}

    sample = request.json["query"]
    return json.dumps(sample)

print()
#print(process_animal("cow"))

if __name__ == "__main__":
    app.run()
