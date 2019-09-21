from aylienapiclient import textapi
import json


# Grab the data from the previous API's
title = "Zebras"
text = "'Zebras (/ˈziːbrə/ ZEE-brə, /ˈzɛbrə/ ZEB-rə)[1] are several species of African equids (horse family) united by their distinctive black-and-white striped coats. Their stripes come in different patterns, unique to each individual. They are generally social animals that live in small harems to large herds. Unlike their closest relatives, horses and donkeys, zebras have never been truly domesticated. There are three species of zebras: the plains zebra, the mountain zebra and the Grévy's zebra. The plains zebra and the mountain zebra belong to the subgenus Hippotigris, while Grévy's zebra is the sole species of subgenus Dolichohippus. The latter resembles an ass, to which zebras are closely related, while the former two look more horse-like. All three belong to the genus Equus, along with other living equids. The unique stripes of zebras make them one of the animals most familiar to people. They occur in a variety of habitats, such as grasslands, savannas, woodlands, thorny scrublands, mountains, and coastal hills. Various anthropogenic factors have had a severe impact on zebra populations, in particular hunting for skins and habitat destruction. Grévy's zebra and the mountain zebra are endangered. While plains zebras are much more plentiful, one subspecies, the quagga, became extinct in the late 19th century – though there is currently a plan, called the Quagga Project, that aims to breed zebras that are phenotypically similar to the quagga in a process called breeding back.'"


def summerizedSentences(title, text):
    # Load the config data
    with open('configs.json', 'r') as data_file:
        config = json.load(data_file)
    
    client = textapi.Client(config["aylienAppID"], config["aylienAppKey"])
    summary = client.Summarize({'title': title, 'text': text, 'sentences_number': 3})
    print(summary['sentences'])


summerizedSentences(title, text)


