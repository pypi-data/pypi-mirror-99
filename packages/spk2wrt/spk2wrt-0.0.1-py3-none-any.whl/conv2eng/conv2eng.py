import numpy as np
import pandas as pd

word_dict = {"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"dollar":'$',"and":'&' , "C M":'CM', "P M":'PM'}

class conve2english:
    """
    def defined_words():
        word_dict = {"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"dollar":'$',"and":'&' , "C M":'CM', "P M":'PM'}
        return word_dict
    """

    def check_word(corpus):
        global word_dict
        #word_dict = conve2english.defined_words()
        word = corpus.split()
        for i in range(0,len(word)):
            if(word[i].lower()) in word_dict.keys():
                replace = word[i].lower()
                replaced_word = word_dict[replace]
                replaced_word = str(replaced_word)
                word[i] = replaced_word
        s = " "
        final_sentence = s.join(word)
        return final_sentence

    def update_word_dict(spoken_word,written_word):
        global word_dict

        #word = conve2english.defined_words
        spoken_word = spoken_word.lower()
        word_dict[spoken_word] = written_word
        return f"The {spoken_word} is replaced with {written_word}"