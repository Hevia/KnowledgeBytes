import wikipediaapi

# Takes parameter WikipediaPageSections
def grab_sections(sections, hash_summaries):
    i = 0
    n = 2
    for s in sections:
        #print(f"We are level {i} and section {s.title}")
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

def create_maps(search_term, language='en'):
    #check that page exists before requesting info 
    wiki_obj = wikipediaapi.Wikipedia(language)
    wiki_page = wiki_obj.page(search_term)
    
    if wiki_page.exists():
        # Store the data in a dict
        hash_summaries = {}
        hash_summaries['summary'] = []
        hash_summaries['summary'].append(wiki_page.summary)
        hash_summaries['title'] = wiki_page.title

        grab_sections(wiki_page.sections, hash_summaries['summary'])
        hash_summaries['summary'] = ''.join(hash_summaries['summary'] )
                
        return hash_summaries
    else:
        return -1

create_maps('Shark')