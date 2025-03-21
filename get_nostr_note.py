#!/usr/bin/env python

import uuid
import asyncio
import tornado.ioloop
import json

from typing import List, Dict, Any, Optional, Union
from rich.console import Console
from rich.table import Table
from tornado import gen
from feedgen.feed import FeedGenerator

from pynostr.base_relay import RelayPolicy
from pynostr.relay_manager import RelayManager
from pynostr.event import EventKind
from pynostr.filters import Filters, FiltersList
from pynostr.message_pool import MessagePool
from pynostr.relay import Relay
from pynostr.utils import get_public_key
from pynostr.key import PublicKey

async def get_profile_info(pubkey: PublicKey, relay_url: str, io_loop=None, timeout: int = 5) -> Optional[Dict[str, Any]]:
    """
    Fetch profile information for a Nostr public key using the existing infrastructure.
    
    Args:
        pubkey: The PublicKey object
        relay_url: Relay websocket URL
        io_loop: Existing Tornado IOLoop (optional)
        timeout: Timeout in seconds to wait for responses
        
    Returns:
        Dictionary containing profile information or None if not found
    """
    if io_loop is None:
        io_loop = tornado.ioloop.IOLoop.current()
    
    # Create a message pool specifically for profile data
    profile_message_pool = MessagePool(first_response_only=False)
    policy = RelayPolicy()
    
    # Setup relay with the profile message pool
    relay = Relay(relay_url, profile_message_pool, io_loop, policy, timeout=timeout)
    
    # Create filter for profile metadata (kind 0 events)
    filters = FiltersList([Filters(authors=[pubkey.hex()], kinds=[EventKind.SET_METADATA], limit=1)])
    
    # Generate a subscription ID
    subscription_id = uuid.uuid1().hex
    
    # Add subscription
    relay.add_subscription(subscription_id, filters)
    
    # Connect to relay
    try:
        await relay.connect()
    except gen.Return:
        pass  # This is expected
    
    # Process messages - the message pool should now contain profile events
    event_msgs = profile_message_pool.get_all_events()
    
    profile_content = None
    
    # Look for profile metadata events
    for event_msg in event_msgs:
        if event_msg.event.kind == EventKind.SET_METADATA:
            try:
                # Parse content as JSON
                profile_content = json.loads(event_msg.event.content)
                
                # Add public key information
                profile_content["pubkey"] = pubkey.hex()
                profile_content["npub"] = pubkey.bech32()
                
                break  # Found what we need
            except json.JSONDecodeError:
                print("Error parsing profile content JSON")
    
    return profile_content

# Function to get public key from npub or nip05 (assuming you already have this)
def get_public_key(input_str):
    # Your existing implementation...
    # For this example, I'll assume a simple implementation:
    if input_str.startswith('npub'):
        return PublicKey.from_npub(input_str)
    else:
        # Assuming input_str is a hex string
        return PublicKey.from_hex(input_str)

# Example of how to integrate profile fetching with your existing code
if __name__ == "__main__":
    input_str = input("author (npub or nip05): ")
    author = get_public_key(input_str)
    relay_url = "wss://nostr.wine"
    
    # Create IO loop
    io_loop = tornado.ioloop.IOLoop.current()
    
    # First, fetch profile information
    profile_future = gen.convert_yielded(get_profile_info(author, relay_url, io_loop))
    
    # Run the profile fetch
    try:
        io_loop.run_sync(lambda: profile_future)
        profile = profile_future.result()
    except gen.Return:
        pass
    
    # Display profile info if found
    if profile:
        print("\nProfile information:")
        print(f"Name: {profile.get('name', 'Not provided')}")
        print(f"Display name: {profile.get('display_name', 'Not provided')}")
        print(f"Picture URL: {profile.get('picture', 'Not provided')}")
        print(f"NIP-05: {profile.get('nip05', 'Not provided')}")
        lightning = profile.get('lud16', None)
        if not lightning: lightning = profile.get('lud06', 'Not provided')
        print(f"L: {lightning}")
        print(f"Web: {profile.get('website', 'Not provided')}")
        print(f"About: {profile.get('about', 'Not provided')}")
        print("")
    
    # Now fetch notes as in your original code
    filters = FiltersList(
        [Filters(authors=[author.hex()], kinds=[EventKind.TEXT_NOTE], limit=10)]
    )
    subscription_id = uuid.uuid1().hex
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
        print(f"{(readable_event)}\n\n")
        if len(readable_event['tags']) == 0:
            fe = fg.add_entry()
            fe.id(f"https://snow-services.com/{readable_event['id']}")
            fe.title(readable_event['pubkey'])
            fe.description(readable_event['content'])
            fe.link(href="https://snow-services.com")
        else:
            continue

    #atomfeed = fg.atom_str(pretty=True) # Get the ATOM feed as string
    #fg.atom_file('atom.xml') # Write the ATOM feed to a file
