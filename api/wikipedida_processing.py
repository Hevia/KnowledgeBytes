import wikipediaapi

# Takes parameter WikipediaPageSections
def grab_sections(sections):
    i = 0
    ret_sections = {}
    for s in sections:
        #print(f"We are level {i} and section {s.title}")
        #i += 1  
        #
        ret_sections[s.title] = []
        ret_sections[s.title].append(s.text)
        grab_sub_sections(ret_sections[s.title], s.sections)

        if i == 3: 
            return ret_sections
    return ret_sections

def grab_sub_sections(ret_sections, sub_sections):
        for l in sub_sections:
            ret_sections.append(l.text)
        return

def create_maps(search_term):
    #check that page exists before requesting info 
    wiki_obj = wikipediaapi.Wikipedia('en')
    wiki_page = wiki_obj.page(search_term)
    
    if wiki_page.exists():
        
        hash_summaries = {}
        hash_summaries['summary'] = wiki_page.summary
        hash_summaries['title'] = wiki_page.title
        section_map = grab_sections(wiki_page.sections)
    else:
        return -1

create_maps()
