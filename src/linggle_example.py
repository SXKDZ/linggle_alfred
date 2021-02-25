import re
import sys
import requests
from workflow import Workflow, ICON_WEB


def strip_html(html):
    p = re.compile(r'<.*?>')
    return p.sub('', html)


def main(wf):
    s = requests.Session()
    
    query = wf.args[0]
    query_load = requests.utils.quote(query)
    payload = {'q': query, 'maxResults': 20}

    proxies = {
        'http': 'http://127.0.0.1:1087',
        'https': 'http://127.0.0.1:1087',
    }

    try:
        answer = s.get('https://www.googleapis.com/books/v1/volumes', params=payload, proxies=proxies).json()
        if int(answer['totalItems']) == 0:
            wf.add_item(
                title='No Examples',
                subtitle='Try another search',
                valid=False,
                icon='icon.png'
            )
        else:
            for item in answer['items']:
                try:
                    phrase = item['searchInfo']['textSnippet']
                    phrase = strip_html(phrase)
                    wf.add_item(
                        title=phrase,
                        arg=phrase,
                        valid=True,
                        icon='icon.png'
                    )
                except KeyError:
                    pass
    
    except Exception as e:
        wf.add_item(
            title='Inquiry Error: {}'.format(e),
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
