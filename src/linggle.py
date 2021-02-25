import sys
import json
import time
import requests
from workflow import Workflow, ICON_WEB

def main(wf):
    s = requests.Session()

    query = wf.args[0]
    query_load = requests.utils.quote(query)
    try:
        answer = s.get('https://linggle.com/api/ngram/{}'.format(query_load)).json()
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
        arg='https://linggle.com/?q={}'.format(query_load)
    )
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
