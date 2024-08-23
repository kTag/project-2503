from feedgen.feed import FeedGenerator
fg = FeedGenerator()
fg.id('https://snow-services.com')
fg.title('kTag Personal Nostr Feed')
fg.author( {'name':'kTag','email':'sdf@sdf.com'} )
fg.link( href='https://github.com/kTag/project-2503', rel='alternate' )
fg.logo('https://raw.githubusercontent.com/kTag/project-2503/nostr/onektag.png')
fg.subtitle('Nostr Feed')
fg.link( href='https://snow-services.com', rel='self' )
fg.language('en')

fe = fg.add_entry()
fe.id('https://snow-services.com/1234')
fe.title('First Entry')
fe.description('This is a long entry to test our RSS feed')
fe.link(href="https://snow-services.com")

atomfeed = fg.atom_str(pretty=True) # Get the ATOM feed as string
fg.atom_file('atom.xml') # Write the ATOM feed to a file
