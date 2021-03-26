#!/usr/local/bin/python3
import webbrowser
import sys

service_mapping = {
    'prime': {
        'base_url': "https://www.primevideo.com",
        'search_url': "https://www.primevideo.com/search/ref=atv_nb_sr?phrase="
    },
    'hotstar': {
        'base_url': "https://hotstar.com",
        'search_url': "https://www.hotstar.com/in/search?q="
    }
}

if len(sys.argv[1:]) > 0 and sys.argv[1] in service_mapping.keys():
    service = sys.argv[1]
    artifact = '+'.join(sys.argv[2:]).lower()

    base_url = service_mapping.get(service)['base_url']

    if artifact != '':
        search_url = service_mapping.get(service)['search_url'].replace('=',f'={artifact}')
        webbrowser.open(search_url)
    else:
        webbrowser.open(base_url)
else:
    exit("Syntax: python streaming.py {streaming_service ('prime', 'hotstar')} {artifact}")
