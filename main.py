import urllib.request, urllib.parse, urllib.error
import logging

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

LOGGER = logging.getLogger(__name__)

def urlencode(q):
    return urllib.parse.urlencode(q)

def url_safe_chunk(q):
    return urllib.parse.quote_plus(q)

class PonsExtension(Extension):

    def __init__(self):
        super(PonsExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = list()

        if event.get_argument():
            LOGGER.info('Word Pons search for "{}"'.format(event.get_argument()))
            items.append(
                ExtensionResultItem(
                    icon='images/icon.png',
                    name='Define words on Pons',
                    description='Define words "{}".'.format(event.get_argument()),
                    on_enter=OpenUrlAction(
                        'https://en.pons.com/translate/' + extension.preferences["source"] + "-" + extension.preferences["target"] + '/{}'.format(url_safe_chunk(event.get_argument())) + '?{}'.format(urlencode({ 'bidir': '1' }))
                    )
                )
            )

        return RenderResultListAction(items)

if __name__ == '__main__':
    PonsExtension().run()
