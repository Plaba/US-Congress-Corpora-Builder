import nltk
import re
import os

from nltk.tokenize import RegexpTokenizer

try:
    from nltk.corpus import words
except:
    nltk.download('words')
    from nltk.corpus import words

try:
    from nltk.corpus import reuters
except:
    nltk.download('reuters')
    from nltk.corpus import reuters
CHAR_LIST="QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm"

def get_word_after_index(text, index):
    answer = ""
    for c in text[index + 1 : ]:
        if c in CHAR_LIST:
            answer += c
        else:
            break
    return answer

def get_word_before_index(text, index):
    answer = ""
    for c in reversed(text[ : index]):
        if c in CHAR_LIST:
            answer += c
        else:
            break
    return answer[::-1]

def find(text, char):
    for i, ltr in enumerate(text):
        if ltr == char:
            yield i
   
vocab = set(words.words())
vocab.update(set(reuters.words()))

def fix_text(text):
    num_deleted = 0
    for i in find(text, "-"):
        before = get_word_before_index(text, i - num_deleted)
        after = get_word_after_index(text, i - num_deleted)

        if len(before) > 0 and len(after) > 0 and (before + after).lower() in vocab:
           
            text = text[:i - num_deleted]+text[i+1-num_deleted:]
            num_deleted += 1
    return text, num_deleted


def main():

    directory = r'transcripts-txt/'
    tokenizer = RegexpTokenizer(r'(?<=[ "\:\.\?\!\)\(])[a-zA-Z]+(?=[ \:\.\?\!\)\(])')
    for filename in os.listdir(directory):
        with open(f"transcripts-txt/{filename}", "r") as file:
            text = file.read()
            vocab.update(set(tokenizer.tokenize(text)))
    for word in list(vocab):
        vocab.remove(word)
        vocab.add(word.lower())
    print(f"Built wordlist: {len(vocab)} words.")
    for filename in os.listdir(directory):
        text = ""
        num_deleted = 0

        with open(f"transcripts-txt/{filename}", "r") as file:
            text = file.read()

            text, num_deleted = fix_text(text)
        with open(f"transcripts-txt/{filename}", "w") as file:
            file.write(text)
        print(f"Fixed {num_deleted} hyphens in file {filename}")
        

if __name__ == "__main__":
    main()
        