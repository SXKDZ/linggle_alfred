import sys
import json
import time
import requests
from workflow import Workflow, ICON_WEB

def main(wf):
    s = requests.Session()
    r = s.get('https://www.linggle.com/')

    headers = {
        'X-CSRFToken': r.cookies['csrftoken'],
        'Referer': 'https://www.linggle.com/',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    query = wf.args[0]
    query_load = {
        'query': query,
        'time': int(round(time.time() * 1000))
    }
    try:
        answer = s.post('https://www.linggle.com/query/', data=json.dumps(query_load), headers=headers).json()
        if len(answer['ngrams']) == 0:
            wf.add_item(
                title='No Results',
                subtitle='Modify your search',
                valid=False,
                icon='icon.png'
            )
        else:
            total = 0
            for item in answer['ngrams']:
                total += item[1]
            
            for item in answer['ngrams'][:20]:
                # print(item)
                phrase = item[0]
                subtitle = '{:.2f}% | {}'.format(float(item[1]) * 100 / total, item[1])
                wf.add_item(
                    title=phrase,
                    subtitle=subtitle,
                    arg=phrase,
                    valid=True,
                    icon='icon.png'
                )
    except:
        wf.add_item(
            title='Inquiry Error',
            subtitle='Modify your search',
            valid=False,
            icon='icon.png'
        )
    wf.add_item(
        title='Visit Linggle',
        subtitle='Open browser for Linggle',
        icon=ICON_WEB,
        valid=True,
        arg='https://www.linggle.com'
    )
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
