from aylien import summerizedSentences
from azure_processing import grab_key_phrases
from wikipedia_processing import create_maps
import json

def checkKey(dict, key): 
    if key in dict.keys(): 
        return True
    else: 
        return False

def summarize_animals(wiki_data, wolfram_data, language="en"):
    animal_summary = {}

    # Grab the scientific name. Given by the Wolfram Alpha API
    if not wolfram_data:
        bio_prop = "biological properties"
        lifespan = "lifespan"
        #animal_summary["wolfram-success"] = True
        animal_summary["image url"] = wolfram_data["image url"] if checkKey(wolfram_data, "image url") else ""
        animal_summary["scientific_name"] = wolfram_data["scientific name"] if checkKey(wolfram_data, "scientific name") else ""
        animal_summary["taxonomy"] = wolfram_data["Taxonomy"] if checkKey(wolfram_data, "Taxonomy") else ""
        animal_summary["lifespan"] = f"The average lifespan is {wolfram_data[bio_prop][lifespan]}"  if checkKey(wolfram_data, "biological properties") else ""
    else:
        #animal_summary["wolfram-success"] = False
        pass

    # Organize and grab the Wikipedia data + making sure the wikipedia data exists
    if wiki_data['exists']:
        animal_summary['title'] = wiki_data['title']
        animal_summary["summary"] = summerizedSentences(wiki_data["title"], wiki_data["summary"])
        animal_summary['text'] = summerizedSentences(wiki_data["title"], wiki_data["text"])
        animal_summary["related"] = grab_key_phrases(wiki_data["summary"])
        #animal_summary['wiki-url'] = wiki_data['wiki-url']
        #animal_summary['wiki-success'] = True
    else:
        #animal_summary['wiki-success'] = False
        pass
    
    animal_summary["success"] = True
    return animal_summary


def summerize_cities(wiki_data, wolfram_data, language="en"):
    city_summary = {}

    if not wolfram_data:
        #city_summary["wolfram-success"] = True
        pass
    else:
        #city_summary["wolfram-success"] = False
        pass

    # Organize and grab the Wikipedia data + making sure the wikipedia data exists
    if wiki_data['exists']:
        city_summary['title'] = wiki_data['title']
        city_summary["summary"] = summerizedSentences(wiki_data["title"], wiki_data["summary"])
        city_summary['text'] = summerizedSentences(wiki_data["title"], wiki_data["text"])
        city_summary["related"] = grab_key_phrases(wiki_data["summary"])
        #city_summary['wiki-url'] = wiki_data['wiki-url']
        #city_summary['wiki-success'] = True
    else:
        #city_summary['wiki-success'] = False
        pass

   

    return city_summary

def summarize_planets(wiki_data, wolfram_data, language="en"):
    planet_summary = {}

    if wiki_data['exists']:
        planet_summary['title'] = wiki_data['title']
        planet_summary["summary"] = summerizedSentences(wiki_data["title"], wiki_data["summary"])
        planet_summary['text'] = summerizedSentences(wiki_data["title"], wiki_data["text"])
        planet_summary["related"] = grab_key_phrases(wiki_data["summary"])
        #planet_summary['wiki-url'] = wiki_data['wiki-url']
        #planet_summary['wiki-success'] = True
    else:
        #planet_summary['wiki-success'] = False
        pass

    if not wolfram_data:
        planet_summary["image url"] = wolfram_data["image url"] if checkKey(wolfram_data, "image url") else ""
        planet_summary["atmospheric data"] = wolfram_data["atmospheric data"] if checkKey(wolfram_data, "atmospheric data") else ""
        pass
    else:
        #city_summary["wolfram-success"] = False
        pass


    

    return planet_summary

def summarize_person(wiki_data, wolfram_data, language="en"):
    person_summary = {}

    if not wolfram_data:
        person_summary["basic information"] = None
        pass
    else:
        #city_summary["wolfram-success"] = False
        pass


    if wiki_data['exists']:
        person_summary['title'] = wiki_data['title']
        person_summary["summary"] = summerizedSentences(wiki_data["title"], wiki_data["summary"])
        person_summary['text'] = summerizedSentences(wiki_data["title"], wiki_data["text"])
        person_summary["related"] = grab_key_phrases(wiki_data["summary"])
        #person_summary['wiki-url'] = wiki_data['wiki-url']
        #person_summary['wiki-success'] = True
    else:
        #person_summary['wiki-success'] = False
        pass

    return person_summary

