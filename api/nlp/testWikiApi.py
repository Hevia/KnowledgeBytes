import wikipediaapi


wiki_obj = wikipediaapi.Wikipedia('en')

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



wiki_page = wiki_obj.page('Shark')
def create_maps():
    #check that page exists before requesting info 
    if wiki_page.exists():
        
        hash_summaries = {}
        #use title as key to retreive summary
        hash_summaries[wiki_page.title] = wiki_page.summary
        hash_titles = {}
        hash_titles["title"] = wiki_page.title
        # print("Page - Exists: %s" % wiki_page.exists())

        # print("Page - Title: %s" % wiki_page.title)

        # print("Page - Summary: %s" % wiki_page.summary[0:300])
        
        section_map = grab_sections(wiki_page.sections)

    else:
        return -1

create_maps()
