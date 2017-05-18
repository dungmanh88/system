def printer_error(s):
    return "%d/%d" % (sum([char > "m" for char in s]),len(s))

if __name__ == "__main__":
    print printer_error("aaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbmmmmmmmmmmmmmmmmmmmxyz")
