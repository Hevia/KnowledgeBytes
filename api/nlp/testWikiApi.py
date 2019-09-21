import wikipediaapi
# create wiki object with param lang, and as for page by official name
# spaces in names are underscores


wiki_obj = wikipediaapi.Wikipedia('en')



wiki_page = wiki_obj.page('Shark')
#check that page exists before requesting info
if wiki_page.exists():
    print("Page - Exists: %s" % wiki_page.exists())

    print("Page - Title: %s" % wiki_page.title)

    print("Page - Summary: %s" % wiki_page.summary[0:300])

    def print_sections(sections, level=0):
        for s in sections:
            if sections == 3:
                break
            print("%s\n%s\n\n" % (s.title, s.text))
            print_sections(s.sections, level + 1)

    print_sections(wiki_page.sections)

    #wiki_html = wikipediaapi.Wikipedia(
    #    language='cs',
    #    extract_format=wikipediaapi.ExtractFormat.HTML
    #)

    page_sharks = wiki_html.page('Sharks')
    print(wiki_page.text)

    #p_html = wiki_html.page("Sharks")
    #print(p_html.text)
