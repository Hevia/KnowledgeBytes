from aylienapiclient import textapi
import json


def summerizedSentences(title, text):
    # Load the config data
    with open('configs.json', 'r') as data_file:
        config = json.load(data_file)
    
    print(len(text))
    n = 5
    client = textapi.Client(config["aylienAppID"], config["aylienAppKey"])
    summary = client.Summarize({'title': title, 'text': text, 'sentences_number': n})

    for i in summary['sentences']:
        print(i)
        print('\n')

    return summary['sentences']



