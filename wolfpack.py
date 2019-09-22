import xml.dom.minidom as minidom
import requests, json

with open("configs.json") as conf:
    config = json.load(conf)

wolfram_app_id = config["wolfram_id"]


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
    #print(ps)

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

        return {"population" : population_stats, "location" : location, "economy" : economic_properties, "geography" : geographic_properties, "nickname" : nickname, "notable people" : notable_people}

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
           

        return {"orbital properties" : orbital_properties, "physical properties" : physical_properties, "atmospheric data" : atmospheric_data, "image url" : image_url} 

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
    #print(pods)

    image_url = ""
    facts = []
    physical_characteristics = {}
    family = {}

    for pod in pods:
        #print()
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
                #print(propstring)
                members = [p.strip() for p in propstring.split('|')]
                family[str(sub.getAttribute("title"))] = members
            
        return {"basic information" : basic_info, "image url" : image_url, "facts" : facts, "physical characteristics" : physical_characteristics, "family" : family} 

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

            #print(taxonomy)            


    return {"scientific name" : scientific_name, "Taxonomy" : taxonomy, "biological properties" : biological_properties} 
