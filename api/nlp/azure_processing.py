from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
import json

def grab_key_phrases(text):
    # Load the config keys
    with open('configs.json', 'r') as data_file:
            config = json.load(data_file) 

    credentials = CognitiveServicesCredentials(config["azure_key"])
    text_analytics = TextAnalyticsClient(endpoint=config["azure_endpoint"], credentials=credentials)

    documents = [
        {
            "id": "1",
            "language": "en",
            "text": text
        }
    ]

    response = text_analytics.key_phrases(documents=documents)

    retval = []
    for document in response.documents:
        for phrase in document.key_phrases:
            retval.append(phrase)
    
    if len(retval) > 5:
        return retval[:5]
    else:
        return retval

