Start Server:

import sws

sws.start_server(5000, 5000)

Stream HTML:
Previous and:

sws.stream_html('<p>test</p>')

Or:

sws.stream_html(sws.load_file('template.html'))

