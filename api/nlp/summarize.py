from aylien import summerizedSentences
from azure_processing import grab_key_phrases
import json

with open('test_data.json', 'r') as data_file:
        data = json.load(data_file)

def summerize_animals(data):
    animal_summary = {}
    # Create a summary from Wikipedia
    animal_summary["summary"] = summerizedSentences(data["title"], data["text"])

    # Grab related topics from the text
    animal_summary["related"] = grab_key_phrases(data["text"])

    # Grab the scientific name. Given by the Wolfram Alpha API
    animal_summary["scientific_name"] = None
    print(animal_summary)



summerize_animals(data)
