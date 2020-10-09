# -*- coding: utf-8 -*-


import re
from collections import Counter
import os


class grammerspell_checker():

  def __init__(self,dict_filepath,inp_filepath,out_filepath):
    self.WORDS = Counter(self.words(open(dict_filepath).read()))
    self.input_filepath = inp_filepath
    self.out_filepath = out_filepath

  def checker(self):
    corrected_text = None
    with open(self.input_filepath,"r") as freader:
      input_text = freader.read()
    if os.path.exists(self.out_filepath):
      print("file existing, deleting...")
      try:
        os.remove(self.out_filepath)
        print("file deleted")
      except:
        print("file cannot be deleted")
    else:
      print("file existed")
      for i in input_text.split(" "):
        temp_spellword = correction(i)
        with open(self.out_filepath,"a") as f:
          f.write(temp_spellword)
          f.write(" ")
      with open(self.out_filepath,"r") as fread:
        corrected_text = fread.read()
    
    return corrected_text

  def words(self,text): return re.findall(r'\w+', text.lower())

  def P(self,word): 

      "Probability of 'word'."
      N=sum(self.WORDS.values())
      return self.WORDS[word] / N

  def correction(self,word): 
      "Most probable spelling correction for word."
      return max(self.candidates(word), key=self.P)

  def candidates(self,word): 
      "Generate possible spelling corrections for word."
      return (self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word])

  def known(self,words): 
      "The subset of `words` that appear in the dictionary of WORDS."
      return set(w for w in words if w in self.WORDS)

  def edits1(self,word):
      "All edits that are one edit away from `word`."
      letters    = 'abcdefghijklmnopqrstuvwxyz'
      splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
      deletes    = [L + R[1:]               for L, R in splits if R]
      transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
      replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
      inserts    = [L + c + R               for L, R in splits for c in letters]
      return set(deletes + transposes + replaces + inserts)

  def edits2(self,word):
    "All edits that are two edits away from 'word'."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

if __name__ == "__main__":

  
  cur_path = os.getcwd()
  dict_filepath = os.path.join(cur_path,"dictionary.txt")
  input_filepath = os.path.join(cur_path,"Assignment_Sampledata.txt")
  out_filepath = os.path.join(cur_path,"out.txt")
  speller = grammerspell_checker(dict_filepath,input_filepath,out_filepath)
  output = speller.checker()
  output
