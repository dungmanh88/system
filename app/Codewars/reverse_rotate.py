def revrot(strng, sz):
    strng = strng.strip()
    if sz <= 0 or len(strng) == 0 or sz > len(strng):    return ""
    total_chunks = len(strng) / sz
    result = ""
    index = 0
    while index < len(strng):
        chunk = strng[index:index+sz]
        print chunk
        print "index %s" % index
        if len(chunk) >= sz:
          sum_digits = sum(map(int,list(chunk)))
          if sum_digits % 2 == 0:
              result += chunk[::-1]
          else:
              result += chunk[1:] + chunk[0]
        else: break
        index = index+sz
    return result

def revrot(s, n, res=""):
    if not s or n < 1 or n > len(s):
        return ""

    while len(s) >= n:
        group = s[:n]
        if sum([int(d)**3 for d in group]) % 2 == 0:
            res += group[::-1]
        else:
            res += group[1:] + group[0]
        s = s[n:]

    return res

if __name__ == "__main__":
    print revrot("733049910872815764", 5)
