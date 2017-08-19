import os
import sys

def friendly_file_size(bytes):
    if bytes <= 1: return "%d %s" % (bytes, "Byte")
    elif bytes > 1 and bytes < 1024: return "%d %s" % (bytes, "Bytes")
    elif bytes >= 1024 and bytes < 1024 * 1024: return "%.1f %s" % (bytes/1024.0, "KB")
    elif bytes >= 1024 * 1024 and bytes < 1024 * 1024 * 1024: return "%.1f %s" % (bytes/1024/1024.0, "MB")
    elif bytes >= 1024 * 1024 * 1024 and bytes < 1024 * 1024 * 1024 * 1024: return "%.1f %s" % (bytes/1024/1024/1024.0, "GB")
    else: return "Too large"

starting_point = "."
if len(sys.argv) == 2:
    starting_point = sys.argv[1]

allfiles = os.listdir(starting_point)
prefix = starting_point

while prefix[-1] == "/":
    prefix = prefix[:len(prefix)-1]

for files in allfiles:
    files = prefix + "/" + files
    if os.path.isdir(files):
        print "DIR %s %s %s" % (friendly_file_size(os.path.getsize(files)),os.path.getctime(files), files)
    else:
        print "FILE %s %s %s" % (friendly_file_size(os.path.getsize(files)),os.path.getctime(files), files)
