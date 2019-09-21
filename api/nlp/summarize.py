from aylien import summerizedSentences
from azure_processing import grab_key_phrases
from wikipedia_processing import create_maps
import json

with open('test_data.json', 'r') as data_file:
        data = json.load(data_file)

def summerize_animals(wiki_data, wolfram_data):
    animal_summary = {}

    # Organize and grab the Wikipedia data
    if wiki_data['exists']:
        animal_summary['title'] = wiki_data['title']
        animal_summary["summary"] = summerizedSentences(wiki_data["title"], wiki_data["summary"])
        animal_summary['text'] = summerizedSentences(wiki_data["title"], wiki_data["text"])
        animal_summary["related"] = grab_key_phrases(wiki_data["summary"])
        animal_summary['wiki-url'] = wiki_data['wiki-url']

    # Grab the scientific name. Given by the Wolfram Alpha API
    animal_summary["scientific_name"] = []
    

    return animal_summary


def summerize_cities(wiki_data, wolfram_data):
    pass

def summerize_planets(wiki_data, wolfram_data):
    pass

def summerize_person(wiki_data, wolfram_data):
    pass

summerize_animals(create_maps('Saturn'))
