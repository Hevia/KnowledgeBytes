from aylien import summerizedSentences
from azure_processing import grab_key_phrases
from wikipedia_processing import create_maps
import json

with open('test_data.json', 'r') as data_file:
        data = json.load(data_file)

def summerize_animals(data):
    animal_summary = {}
    # Create a summary from Wikipedia
    animal_summary["summary"] = summerizedSentences(data["title"], data["summary"])
    animal_summary['text'] = summerizedSentences(data["title"], data["text"])

    # Grab related topics from the text
    animal_summary["related"] = grab_key_phrases(data["summary"])

    # Grab the scientific name. Given by the Wolfram Alpha API
    animal_summary["scientific_name"] = []
    
    for i in animal_summary:
        for j in animal_summary[i]:
            print(j)



summerize_animals(create_maps('Shark'))
