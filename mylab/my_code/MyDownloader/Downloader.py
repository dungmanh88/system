import sys
import requests

def download(url):
    # if len(sys.argv) != 2:
    #     print "Usage python Downloader.py URL"
    #     sys.exit(1)
    #
    # url = sys.argv[1].strip()
    url = url.strip()
    if url == "":
        print "Usage python Downloader.py URL"
        sys.exit(2)

    req = requests.get(url, stream=True)
    req.raise_for_status()

    output_file = url[url.rindex("/")+1:]

    if req.status_code == 200:
        file_mode = "wb" if req.headers['Content-Type'].find("text") == -1 else "w"
        with open(output_file, file_mode) as f:
            for chunk in req.iter_content(chunk_size=102400):
                print "Writing a chunk"
                f.write(chunk)
            else:
                print "Finish downloading into %s" % output_file
    else:
        print "Request not 200 status code"
