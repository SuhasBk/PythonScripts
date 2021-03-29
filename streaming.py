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

if len(sys.argv[1:]) > 0 and sys.argv[1].lower() in (*service_mapping.keys(), 'all'):
    service = sys.argv[1].lower()
    artifact = '+'.join(sys.argv[2:]).lower()

    if service == 'all':
        if artifact:
            for streaming_service in service_mapping.keys():
                search_url = service_mapping.get(streaming_service)['search_url'].replace('=',f'={artifact}')
                webbrowser.open(search_url)
        else:
            for streaming_service in service_mapping.keys():
                base_url = service_mapping.get(streaming_service)['base_url']
                webbrowser.open(base_url)
    else:
        if artifact:
            search_url = service_mapping.get(service)['search_url'].replace('=',f'={artifact}')
            webbrowser.open(search_url)
        else:
            base_url = service_mapping.get(service)['base_url']
            webbrowser.open(base_url)
else:
    exit("Syntax: python streaming.py {streaming_service ('prime', 'hotstar', 'all')} {artifact}")
