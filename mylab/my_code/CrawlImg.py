import urllib2
from HTMLParser import HTMLParser
import sys
import MyDownloader.Downloader as mdownload

img_filterd_list=[]
reload(sys)
sys.setdefaultencoding("utf8")

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print "Encounter a start tag: %s" % tag
        if str(tag) == "img" and attrs.__len__ > 0:
            for a in attrs:
                if a[0] == "src" and a[1].find("http://static.vietdesigner.net/attachments") != -1:
                    img_filterd_list.append(a[1])

def main():
    req = urllib2.Request(url="http://forum.vietdesigner.net/threads/16-full-bo-anh-2-thieu-nu-ben-tuyet-tinh-coc-dang-bi-dan-mang-che-bai.125246/", headers={'User-Agent' : "Magic Browser"})
    con = urllib2.urlopen(req)
    print "Result code: %s" % str(con.getcode())
    data = con.read()
    # data is html
    print "Data: %s" % data
    # use parser to parse html output
    parser = MyHTMLParser()
    parser.feed(data)
    parser.close()

    for img in img_filterd_list:
        print "Image: %s" % img
        img = img[:len(img)-1]
        mdownload.download(img)

if __name__ == "__main__":
    main()
