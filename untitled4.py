# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 01:31:45 2023

@author: Zhengqi Wang
"""
from nltk.stem import PorterStemmer
import re

stemmer = PorterStemmer()

# Define file paths
train_file = 'WSJ_02-21.pos-chunk'
test_file = 'WSJ_23.pos'

# Output file paths
train_feature_file = 'training.feature'
test_feature_file = 'test.feature'

noun_phrase_dict = {
    r'^NN': 'I-NP',      
    r'^NNS': 'I-NP',      
    r'^NNP': 'I-NP',      
    r'^NNPS': 'I-NP',     
    r'^DT': 'B-NP',        
    r'^JJ': 'B-NP',       
}


def apply_np_special_dict(word, pos):
    for pattern, tag in noun_phrase_dict.items():
        if re.match(pattern, pos):
            return tag
    return 'O' 



def create_feature_file(input_file, output_file, mode):
    prev_word = ""
    prev_pos = ""
    prev_bio = "@@"
    pre_prev_word = ""
    pre_prev_pos = ""
    with open(input_file, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i] == '\n':
                prev_word = 'empty'
                prev_pos = 'empty'
                if mode == 'train':
                    prev_bio = '@@'
            else:
                if mode == 'train':
                    curr_word, curr_pos, curr_bio = lines[i].strip().split('\t')[:3]
                elif mode == 'test':
                    curr_word, curr_pos = lines[i].strip().split('\t')[:2]
                if i >= len(lines) - 1 or lines[i + 1] == '\n':
                    next_word, next_pos = ('empty', 'empty')
                else:
                    next_word, next_pos = lines[i + 1].strip().split('\t')[:2]

                # Get previous to previous word and its POS tag
                if i < 2 or lines[i - 2] == '\n':
                    pre_prev_word, pre_prev_pos = ('empty', 'empty')
                else:
                    pre_prev_word, pre_prev_pos = lines[i - 2].strip().split('\t')[:2]

                # Get next to next word and its POS tag
                if i >= len(lines) - 2 or lines[i + 2] == '\n':
                    next_next_word, next_next_pos = ('empty', 'empty')
                else:
                    next_next_word, next_next_pos = lines[i + 2].strip().split('\t')[:2]
                if mode == 'train':
                    write_output(output_file, curr_word, curr_pos, curr_bio, prev_word, prev_pos, prev_bio,
                                 pre_prev_word, pre_prev_pos, next_word, next_pos, next_next_word, next_next_pos)
                    prev_bio = curr_bio
                elif mode == 'test':
                    write_test_output(output_file, curr_word, curr_pos, prev_word, prev_pos, prev_bio,
                                      pre_prev_word, pre_prev_pos, next_word, next_pos, next_next_word, next_next_pos)
                prev_word = curr_word
                prev_pos = curr_pos

            if lines[i] == '\n' or i == len(lines) - 1:
                with open(output_file, 'a') as f:
                    f.write('\n')
            
import string
punctuation_chars = set(string.punctuation)


# Function to write output with features and BIO tags
def write_output(output, word, pos, bio, prev_word, prev_pos, prev_bio,
                 pre_prev_word, pre_prev_pos, next_word, next_pos,
                 next_next_word, next_next_pos):
    is_capitalized = int(word.istitle())  # Convert boolean to integer (0 or 1)
    is_punctuation = int(all(char in punctuation_chars for char in word))  # Convert boolean to integer (0 or 1)
    with open(output, 'a') as f: 
        f.write(f'{word}\tPOS={pos}')
        if prev_pos:
            f.write(f"\tPrevious_Pos={prev_pos}")
        if prev_word:
            f.write(f"\tPrevious_Word={prev_word}")
        if prev_bio:
            f.write(f"\tPrevious_Bio={prev_bio}")
        if pre_prev_word:
            f.write(f"\tPrevious_two_word={pre_prev_word}")
        if pre_prev_pos:
            f.write(f"\tPrevious_two_pos={pre_prev_pos}")
        if next_word:
            f.write(f"\tNext_word={next_word}")
        if next_pos:
            f.write(f"\tNext_pos={next_pos}")
        if next_next_word:
            f.write(f"\tNext_two_word={next_next_word}")
        if next_next_pos:
            f.write(f"\tNext_two_pos={next_next_pos}")
        f.write(f"\tIs_Capitalized={is_capitalized}")
        f.write(f"\tIs_Punctuation={is_punctuation}")
        if bio:
            f.write(f"\t{bio}")
        f.write("\n")

def write_test_output(output, word, pos, prev_word, prev_pos, prev_bio,
                      pre_prev_word, pre_prev_pos, next_word, next_pos,
                      next_next_word, next_next_pos):
    is_capitalized = int(word.istitle())  # Convert boolean to integer (0 or 1)
    is_punctuation = int(all(char in punctuation_chars for char in word))  # Convert boolean to integer (0 or 1)
    with open(output, 'a') as f:  
        f.write(f"{word}\tPOS={pos}")
        if prev_pos:
            f.write(f"\tPrevious_Pos={prev_pos}")
        if prev_word:
            f.write(f"\tPrevious_Word={prev_word}")
        if prev_bio:
            f.write(f"\tPrevious_Bio={prev_bio}")
        if pre_prev_word:
            f.write(f"\tPrevious_two_word={pre_prev_word}")
        if pre_prev_pos:
            f.write(f"\tPrevious_two_pos={pre_prev_pos}")
        if next_word:
            f.write(f"\tNext_word={next_word}")
        if next_pos:
            f.write(f"\tNext_pos={next_pos}")
        if next_next_word:
            f.write(f"\tNext_two_word={next_next_word}")
        if next_next_pos:
            f.write(f"\tNext_two_pos={next_next_pos}")
        f.write(f"\tIs_Capitalized={is_capitalized}")
        f.write(f"\tIs_Punctuation={is_punctuation}")
        f.write("\n")
    
    
    
# Create the feature files
create_feature_file(test_file, test_feature_file, 'test')
create_feature_file(train_file, train_feature_file, 'train')
