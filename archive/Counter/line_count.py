from sys import argv

script, input_file = argv

def line_count(file_path):
  f = open(file_path)
  lines = 0
  for line in f:
    if not line.strip():
      break
    lines +=1
  return lines

if __name__ == "__main__":
  try:
    print("Line count = {0}".format(line_count(input_file)))
  except:
    print ("Can't open file!")
  
