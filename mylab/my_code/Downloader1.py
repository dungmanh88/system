from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import sys
import requests
import thread
import threading
import urllib

chunks={}

def downloadPartial(url, start_range, end_range):
    req = requests.get(url, stream=True)
    end_range = end_range - 1
    print "url: %s, start_range: %d, end_range: %d" % (url, start_range, end_range)
    req.raise_for_status()
    ### Download chunk into dictionary in seperate thread
    for chunk in req.iter_content(chunk_size=1024):
        chunks[start_range]=chunk

server_accept_range = False

if len(sys.argv) != 3:
    print "Usage Downloader1.py URL NUM_THREAD"
    sys.exit(1)

url = sys.argv[1].strip()
try:
    URLValidator()(url)
except ValidationError:
    print "Please enter an valid url"
    sys.exit(1)

try:
    num_thread = int(sys.argv[2].strip())
except ValueError:
    print "Please enter an integer"
    sys.exit(1)

print "%s %d" % (url, num_thread)

test_accept_range_url = url[:url.rindex("/")]

req = requests.get(test_accept_range_url)
if req.headers.__contains__('Accept-Ranges') and req.headers['Accept-Ranges'] == 'bytes':
    server_accept_range = True

print "server_accept_range: %d" % server_accept_range

if server_accept_range:
    try:
        content_length = int(urllib.urlopen(url).info().getheaders("Content-Length")[0])
    except ValueError:
        print "Cannot convert content_length to int"
        sys.exit(1)
    print "content_length: %s" % content_length

    step = content_length / num_thread
    print "step: %d" % step
    start_range, end_range = 0, 0
    for i in xrange(0, num_thread):
        start_range = end_range
        if step < content_length - end_range and content_length - end_range < 2 * step:
            end_range = start_range + ( content_length - end_range )
        else:
            end_range = start_range + step
        downloadPartial(url, start_range, end_range)

output_file = url[url.rindex("/")+1:]
### Append chunk in dictionary to completed output file.
with open(output_file, "w") as f:
    for key in chunks.keys():
        print "Writing a chunk"
        f.write(chunks[key])
    else:
        print "Finish downloading into %s" % output_file
