from tqdm import tqdm

import time

for x in tqdm(range(100)):
    time.sleep(0.01)
print "Download successfully"
