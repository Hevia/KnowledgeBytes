from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
import json, random

def grab_key_phrases(text, language="en"):
    # Load the config keys
    with open('configs.json', 'r') as data_file:
            config = json.load(data_file) 

    credentials = CognitiveServicesCredentials(config["azure_key"])
    text_analytics = TextAnalyticsClient(endpoint=config["azure_endpoint"], credentials=credentials)

    documents = [
        {
            "id": "1",
            "language": language,
            "text": text
        }
    ]

    response = text_analytics.key_phrases(documents=documents)

    # Append the phrases together
    retval = []
    for document in response.documents:
        for phrase in document.key_phrases:
            retval.append(phrase)

    #TODO: Maybe clean data and remove stop words?
    
    # So we can return some different results each time
    random.shuffle(retval)

    if len(retval) > 5:
        return retval[:5]
    else:
        return retval

