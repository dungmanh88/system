text = "X-DSPAM-Confidence:    0.8475";
first_pos = text.find(":")
num = float(text[first_pos+1:].lstrip())
print "%g" % num
