from aylien import summerizedSentences
from azure_processing import grab_key_phrases
import json

with open('test_data.json', 'r') as data_file:
        data = json.load(data_file)

def summerize_animals(data):
    #aylien_processed = summerizedSentences(data["title"], data["text"]) # Returns key sentences from processed text
    azure_related_topics = grab_key_phrases(data["text"])



summerize_animals(data)
