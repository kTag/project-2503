from feedgen.feed import FeedGenerator
fg = FeedGenerator()
fg.id('https://snow-services.com')
fg.title('kTag Personal Nostr Feed')
fg.author( {'name':'kTag','email':'sdf@sdf.com'} )
fg.link( href='https://github.com/kTag/project-2503', rel='alternate' )
fg.logo('http://ex.com/logo.jpg')
fg.subtitle('Nostr Feed')
fg.link( href='https://snow-services.com', rel='self' )
fg.language('en')

fe = fg.add_entry()
fe.id('http://lernfunk.de/media/654321/1')
fe.title('The First Episode')
fe.description('Description')
fe.link(href="http://lernfunk.de/feed")

atomfeed = fg.atom_str(pretty=True) # Get the ATOM feed as string
fg.atom_file('atom.xml') # Write the ATOM feed to a file
fg.rss_file('rss.xml') # Write the RSS feed to a file
