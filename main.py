import urllib.request, urllib.parse, urllib.error
import logging
import webbrowser
from bs4 import BeautifulSoup
import requests

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

LOGGER = logging.getLogger(__name__)

def urlencode(q):
    return urllib.parse.urlencode(q)

def url_safe_chunk(q):
    return urllib.parse.quote_plus(q)

class PonsExtension(Extension):

    def __init__(self):
        super(PonsExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = list()
        
        query= event.get_argument()
        if query:
            LOGGER.info('Word Pons search for "{}"'.format(event.get_argument()))

            address = f'https://en.pons.com/translate/' + extension.preferences["source"] + "-" + extension.preferences["target"] + '/{}'.format(url_safe_chunk(event.get_argument())) + '?{}'.format(urlencode({ 'bidir': '1' }))
            request = requests.get(address)
            response = BeautifulSoup(request.content, 'html.parser')
            
            try:
                translate = ','.join(i.dt.text.strip()+ ' -> ' + i.dd.text.strip() + '\n' for i in response.find('div', class_='results').find_all('dl', {'class': 'dl-horizontal'})[:3])
            except:
                translate = 'Not found :('            

            data = {
                'name': query,
                'description': translate,
                'address': address
            }

            return RenderResultListAction([
                ExtensionResultItem(icon='images/icon.png',
                    name=data['name'],
                    description=data['description'],
                    on_enter=ExtensionCustomAction(data, keep_app_open=True))
            ])
        
            # items.append(
            #     ExtensionResultItem(
            #         icon='images/icon.png',
            #         name='Define words on Pons',
            #         description='Define words "{}".'.format(event.get_argument()),
            #         on_enter=OpenUrlAction(
            #             'https://en.pons.com/translate/' + extension.preferences["source"] + "-" + extension.preferences["target"] + '/{}'.format(url_safe_chunk(event.get_argument())) + '?{}'.format(urlencode({ 'bidir': '1' }))
            #         )
            #     )
            # )

        else:
            return RenderResultListAction([
                ExtensionResultItem(icon='images/icon.png',
                    name='Search Pons',
                    description='Search for a word in Pons',
                    on_enter=HideWindowAction())
            ])

        return RenderResultListAction(items)

class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()
        return RenderResultListAction([
            ExtensionResultItem(icon='images/icon.png',
                                name=data['name'],
                                description=data['description'],
                                on_enter=webbrowser.open(data['address']))
        ])
    
if __name__ == '__main__':
    PonsExtension().run()
