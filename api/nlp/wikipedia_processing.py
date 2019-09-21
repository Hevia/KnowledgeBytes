import wikipediaapi

# Processes the sections so we can use them for processing
def grab_sections(sections, hash_summaries, n=2):
    i = 0
    n = 2
    for s in sections:
        i += 1 
        hash_summaries.append(s.text)
        grab_sub_sections(hash_summaries, s.sections)

        if i == n: 
            return 
    return 

def grab_sub_sections(hash_summaries, sub_sections):
        for l in sub_sections:
            hash_summaries.append(l.text)
        return

def create_maps(search_term, language='en', n=2):
    #check that page exists before requesting info 
    wiki_obj = wikipediaapi.Wikipedia(language)
    wiki_page = wiki_obj.page(search_term)
    hash_summaries = {}
    
    if wiki_page.exists():
        # Store the data in a dict for later processing
        hash_summaries['title'] = wiki_page.title
        hash_summaries['exists'] = True
        hash_summaries['summary'] = []
        hash_summaries['summary'].append(wiki_page.summary)
        hash_summaries['text'] = []
        hash_summaries['wiki-url'] = wiki_page.fullurl

        # Concat all the text from a specificed amount of sections
        grab_sections(wiki_page.sections, hash_summaries['text'], n)
        hash_summaries['text'] = ''.join(hash_summaries['text']) # One of the faster and more readable methods for string concat
        return hash_summaries
    else:
        hash_summaries['exists'] = False
        return hash_summaries


