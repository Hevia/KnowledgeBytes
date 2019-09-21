from flask import Flask, render_template, request
import xml.dom.minidom as minidom
import requests, json

app = Flask(__name__)

# CONSTANTS
animal = 'a'
person = 'h'
planet = 'p'
cities = 'c'

max_query_lengh = 100

#with open("local/app_id") as f:
#    wolfram_app_id = f.read().strip()

@app.route("/")
def main():
    return render_template("index.html")

def categorize_string(s):
    # TODO
    #print(s)
    url = build_request_url(s, ["Result"])
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

def build_request_url(input_string, options):
    
    url = "http://api.wolframalpha.com/v2/query?appid=" + wolfram_app_id 
    url += "&input=" + input_string
    url += "&format=plaintext"

    for o in options:
        url += "&includepodid=" + o

    return url    

def table_to_dict(table_as_string):
    table_as_dict = {}

    i = 0
    ps = table_as_string.replace('\n', '|').split('|')
    print(ps)

    while i < len(ps) - 1:
        table_as_dict[ps[i].strip()] = ps[i+1].strip()
        i += 2

    return table_as_dict 

def pod_to_plaintext(pod, plaintextField="plaintext"):

    temp = pod.getElementsByTagName("subpod")[0]
    propstring = temp.getElementsByTagName(plaintextField)[0].firstChild.nodeValue
            
    return propstring        

def process_cities(input_string, options=["Population:CityData", "Location:CityData", "EconomicProperties:CityData", "GeographicProperties:CityData", "BasicInformation:CityData", "NotablePeople:CityData"]):
    
    # build request url
    url = build_request_url(input_string, options)

    print(url)

    # do request
    req = requests.get(url)

    # initialize xml
    dt = minidom.parseString(req.text)
    collection = dt.documentElement
    pods = collection.getElementsByTagName("pod")

    for pod in pods:

        # get population stats
        if str(pod.getAttribute("title")) == "Populations":
            propstring = pod_to_plaintext(pod)
            population_stats = table_to_dict(propstring)
            continue 

        # get location data
        if str(pod.getAttribute("title")) == "Location": 
            location = pod_to_plaintext(pod)
            continue

        # get economic data
        if str(pod.getAttribute("title")) == "Economic properties":
            propstring = pod_to_plaintext(pod)
            economic_properties = table_to_dict(propstring)
            continue

        if str(pod.getAttribute("title")) == "Geographic properties": 
            propstring = pod_to_plaintext(pod)
            geographic_properties = table_to_dict(propstring)
            continue

        if str(pod.getAttribute("title")) == "Nickname": 
            nickname = pod_to_plaintext(pod)
            continue

        if "Notable people" in str(pod.getAttribute("title")): 
            notable_people = [p[:p.find('(')].strip() for p in pod_to_plaintext(pod).split('\n')]

        return json.dumps({"population" : population_stats, "location" : location, "economy" : economic_properties, "geography" : geographic_properties, "nickname" : nickname, "notable people" : notable_people})

def process_planet(input_string, options=["BasicPlanetOrbitalPropertiesEntityTriggered:PlanetData", "BasicPlanetPhysicalProperties:PlanetData", "PlanetAtmospheres:PlanetData", "Image:PlanetData"]):

    # build request url
    url = build_request_url(input_string, options)

    print(url)

    # do request
    req = requests.get(url) 

    # initialize xml
    dt = minidom.parseString(req.text)
    collection = dt.documentElement
    pods = collection.getElementsByTagName("pod")

    for pod in pods:

        # get orbital properties
        if str(pod.getAttribute("title")) == "Orbital properties":
            propstring = pod_to_plaintext(pod)
            orbital_properties = table_to_dict(propstring) 
            continue

        # get physical properties
        if str(pod.getAttribute("title")) == "Physical properties":
            propstring = pod_to_plaintext(pod)
            physical_properties = table_to_dict(propstring)
            continue

        # get atmospheric data
        if str(pod.getAttribute("title")) == "Atmosphere":
            propstring = pod_to_plaintext(pod)
            atmospheric_data = table_to_dict(propstring)
            continue

        # get image url
        if str(pod.getAttribute("title")) == "Image": 
            image_url = pod_to_plaintext(pod, plaintextField="imagesource")   
           

        return json.dumps({"orbital properties" : orbital_properties, "physical properties" : physical_properties, "atmospheric data" : atmospheric_data, "image url" : image_url})        

def process_person(input_string, options=["BasicInformation:PeopleData", "Image:PeopleData", "NotableFacts:PeopleData", "PhysicalCharacteristics:PeopleData", "FamilialRelationships:PeopleData"]):
    '''basic info, image, facts, physical caracteristics, family'''

    # build request url
    url = build_request_url(input_string, options)
    print(url)
    req = requests.get(url)


    # xml parsing tools
    dt = minidom.parseString(req.text)
    collection = dt.documentElement
    pods = collection.getElementsByTagName("pod")
    print(pods)

    image_url = ""
    facts = []
    physical_characteristics = {}
    family = {}

    for pod in pods:
        print()
        # get basic info
        if(str(pod.getAttribute("title")) == "Basic information"):
            propstring = pod_to_plaintext(pod)
            basic_info = table_to_dict(propstring) 
            continue

        if(str(pod.getAttribute("title")) == "Image"):
            image_url = pod_to_plaintext(pod, plaintextField="imagesource")
            continue

        if(str(pod.getAttribute("title")) == "Notable facts"):
            factstring = pod_to_plaintext(pod)
            facts = factstring.split('\n')
            continue

        if(str(pod.getAttribute("title")) == "Physical characteristics"):
            propstring = pod_to_plaintext(pod)
            physical_characteristics = table_to_dict(propstring)
            continue

        if(str(pod.getAttribute("title")) == "Familial relationships"):
            subs = pod.getElementsByTagName("subpod")

            for sub in subs:
                propstring = sub.getElementsByTagName("plaintext")[0].firstChild.nodeValue
                print(propstring)
                members = [p.strip() for p in propstring.split('|')]
                family[str(sub.getAttribute("title"))] = members
            
        return json.dumps({"basic information" : basic_info, "image url" : image_url, "facts" : facts, "physical characteristics" : physical_characteristics, "family" : family}) 

def process_animal(input_string, options=["ScientificName:SpeciesData", "Taxonomy:SpeciesData", "SpeciesDataPhysicalProperties"]):    

    # build request url
    url = build_request_url(input_string, options)

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

        # get scientific name
        if str(pod.getAttribute("title")) == "Scientific name":
            scientific_name = pod_to_plaintext(pod)
            continue 

        # Get Biological Properties
        if str(pod.getAttribute("title")) == "Biological properties":

            for sub in pod.getElementsByTagName("subpod"):
                propstring = sub.getElementsByTagName("plaintext")[0].firstChild.nodeValue
                #print(propstring)            

                biological_properties = {**biological_properties, **table_to_dict(propstring)}

            continue

        if str(pod.getAttribute("title")) == "Taxonomy":
            temp = pod.getElementsByTagName("subpod")[0]

            i = 0
            taxstring = temp.getElementsByTagName("plaintext")[0].firstChild.nodeValue

            ts = taxstring.replace('\n', '|').split('|') 
            taxonomy = [] 
            

            for t in ts:

                if i == 1:
                    taxonomy.append(t.strip())

                i = (i+1) % 2

            print(taxonomy)            


    return json.dumps({"scientific name" : scientific_name, "Taxonomy" : taxonomy, "biological properties" : biological_properties})       

@app.route("/search_query", methods=["POST"])
def post_search_query():

    input_string = "Kanye+West"

    # validate input
    if not input_string or len(input_string) > max_query_lengh:
        return(json.encoder({"success" : "false", "message" : "query length too long"}))

    # get category
    category = categorize_string(input_string)

    if category == animal:
        process_animal(input_string)

    return None

@app.route("/sample", methods=["POST"])
def get_sample_query():
    # For testing

    #{"query" : "user_search_term"}

    sample = request.json["query"]

    with open("scripts/data/mock_summary_zebra.json") as f:
        sample = json.load(f.read())

    return sample

#print()
#print(process_animal("cat"))
#print()
#print(process_person("Barack Obama"))
#print()
#print(process_planet("saturn"))
#print()
#print(process_cities("miami"))

post_search_query()

if __name__ == "__main__":
    app.run()
