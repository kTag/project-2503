#!/usr/bin/env python

import uuid

import tornado.ioloop
from rich.console import Console
from rich.table import Table
from tornado import gen
from feedgen.feed import FeedGenerator

from pynostr.base_relay import RelayPolicy
from pynostr.event import EventKind
from pynostr.filters import Filters, FiltersList
from pynostr.message_pool import MessagePool
from pynostr.relay import Relay
from pynostr.utils import get_public_key

if __name__ == "__main__":
    input_str = input("author (npub or nip05): ")
    author = get_public_key(input_str)

    #relay_url = input("relay: ")
    relay_url = "wss://nostr.wine" 

    filters = FiltersList(
        [Filters(authors=[author.hex()], kinds=[EventKind.TEXT_NOTE], limit=10)]
    )

    subscription_id = uuid.uuid1().hex
    io_loop = tornado.ioloop.IOLoop.current()
    message_pool = MessagePool(first_response_only=False)
    policy = RelayPolicy()
    r = Relay(relay_url, message_pool, io_loop, policy, timeout=3)

    r.add_subscription(subscription_id, filters)

    try:
        io_loop.run_sync(r.connect)
    except gen.Return:
        pass
    io_loop.stop()

    event_msgs = message_pool.get_all_events()
    print(f"{r.url} returned {len(event_msgs)} TEXT_NOTEs from {input_str}.")

    fg = FeedGenerator()
    fg.id('https://snow-services.com')
    fg.title('kTag Personal Nostr Feed')
    fg.author( {'name':'kTag','email':'sdf@sdf.com'} )
    fg.link( href='https://github.com/kTag/project-2503', rel='alternate' )
    fg.logo('https://raw.githubusercontent.com/kTag/project-2503/nostr/onektag.png')
    fg.subtitle('Nostr Feed')
    fg.link( href='https://snow-services.com', rel='self' )
    fg.language('en')

    for event_msg in event_msgs[::-1]:
        readable_event=event_msg.event.to_dict()
        if len(fe.tag) == 0:
            fe = fg.add_entry()
            fe.id(f'https://snow-services.com/{readable_event['id']}')
            fe.title(readable_event['pubkey'])
            fe.description(readable_event['content'])
            fe.link(href="https://snow-services.com")
        else:
            continue
        print(f"{(readable_event)}\n\n")

    atomfeed = fg.atom_str(pretty=True) # Get the ATOM feed as string
    fg.atom_file('atom.xml') # Write the ATOM feed to a file
