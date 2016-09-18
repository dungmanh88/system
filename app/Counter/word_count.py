from sys import argv

script, input_file = argv

def word_count(file_path):
  f = open(file_path)
  words = 0
  for line in f:
    if not line.strip():
      break
    word_list_in_line = line.split()
    words += len(word_list_in_line)
  return words

if __name__ == "__main__":
  try:
    print("Word count = {0}".format(word_count(input_file)))
  except:
    print ("Can't open file!")
  
