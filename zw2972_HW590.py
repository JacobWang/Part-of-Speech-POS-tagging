# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 17:21:57 2023

@author: Zhengqi Wang
"""

from nltk.stem import PorterStemmer
import re

stemmer = PorterStemmer()

# Define file paths
train_file = 'WSJ_02-21.pos-chunk'
test_file = 'WSJ_24.pos'

# Output file paths
train_feature_file = 'training.feature'
test_feature_file = 'test.feature'

# Define the special dictionary for NP tags
noun_phrase_dict = {
    r'^NN': 'I-NP',       # Singular Noun
    r'^NNS': 'I-NP',      # Plural Noun
    r'^NNP': 'I-NP',      # Proper Noun (singular)
    r'^NNPS': 'I-NP',     # Proper Noun (plural)
    r'^DT': 'B-NP',        # Determiner
    r'^JJ': 'B-NP',        # Adjective
}

# Function to apply the special dictionary to determine NP tags
def apply_np_special_dict(word, pos):
    for pattern, tag in noun_phrase_dict.items():
        if re.match(pattern, pos):
            return tag
    return 'O'  # Default tag (not part of a noun phrase)

# Function to extract features from a word
def extract_features(word_info, prev_word_info, prev_2_word_info, next_word_info, next_2_word_info):
    word_str, word_pos = word_info
    word_stem = stemmer.stem(word_str)

    # Determine the NP tag using the special dictionary
    np_tag = apply_np_special_dict(word_str, word_pos)

    features = [word_str, f'POS={word_pos}', f'WORD_STEM={word_stem}', f'NP_TAG={np_tag}']

    if prev_word_info:
        prev_word_str, prev_word_pos = prev_word_info
        prev_word_stem = stemmer.stem(prev_word_str)
        prev_np_tag = apply_np_special_dict(prev_word_str, prev_word_pos)
        features.extend([
            f'PREVIOUS_POS={prev_word_pos}',
            f'PREVIOUS_WORD={prev_word_str}',
            f'PREVIOUS_WORD_STEM={prev_word_stem}',
            f'PREVIOUS_NP_TAG={prev_np_tag}',
        ])
    else:
        features.extend([
            'PREVIOUS_POS=Begin_of_Sent',
            'PREVIOUS_WORD=Begin_of_Sent',
            'PREVIOUS_WORD_STEM=Begin_of_Sent',
            'PREVIOUS_NP_TAG=Begin_of_Sent',
        ])

    if prev_2_word_info:
        prev_2_word_str, prev_2_word_pos = prev_2_word_info
        prev_2_word_stem = stemmer.stem(prev_2_word_str)
        prev_2_np_tag = apply_np_special_dict(prev_2_word_str, prev_2_word_pos)
        features.extend([
            f'PREVIOUS_2_POS={prev_2_word_pos}',
            f'PREVIOUS_2_WORD={prev_2_word_str}',
            f'PREVIOUS_2_WORD_STEM={prev_2_word_stem}',
            f'PREVIOUS_2_NP_TAG={prev_2_np_tag}',
        ])
    else:
        features.extend([
            'PREVIOUS_2_POS=Begin_of_Sent',
            'PREVIOUS_2_WORD=Begin_of_Sent',
            'PREVIOUS_2_WORD_STEM=Begin_of_Sent',
            'PREVIOUS_2_NP_TAG=Begin_of_Sent',
        ])

    if next_word_info:
        next_word_str, next_word_pos = next_word_info
        next_word_stem = stemmer.stem(next_word_str)
        next_np_tag = apply_np_special_dict(next_word_str, next_word_pos)
        features.extend([
            f'NEXT_POS={next_word_pos}',
            f'NEXT_WORD={next_word_str}',
            f'NEXT_WORD_STEM={next_word_stem}',
            f'NEXT_NP_TAG={next_np_tag}',
        ])
    else:
        features.extend([
            'NEXT_POS=End_of_Sent',
            'NEXT_WORD=End_of_Sent',
            'NEXT_WORD_STEM=End_of_Sent',
            'NEXT_NP_TAG=End_of_Sent',
        ])

    if next_2_word_info:
        next_2_word_str, next_2_word_pos = next_2_word_info
        next_2_word_stem = stemmer.stem(next_2_word_str)
        next_2_np_tag = apply_np_special_dict(next_2_word_str, next_2_word_pos)
        features.extend([
            f'NEXT_2_POS={next_2_word_pos}',
            f'NEXT_2_WORD={next_2_word_str}',
            f'NEXT_2_WORD_STEM={next_2_word_stem}',
            f'NEXT_2_NP_TAG={next_2_np_tag}',
        ])
    else:
        features.extend([
            'NEXT_2_POS=End_of_Sent',
            'NEXT_2_WORD=End_of_Sent',
            'NEXT_2_WORD_STEM=End_of_Sent',
            'NEXT_2_NP_TAG=End_of_Sent',
        ])

    return features

# Function to create the feature file
def create_feature_file(input_file, output_file):
    with open(input_file, "r") as f:
        lines = f.readlines()

    with open(output_file, 'w') as out_f:
        prev_word_info, prev_2_word_info = None, None
        sentence = []

        for line in lines:
            line = line.strip()
            if not line:
                if sentence:
                    out_f.write('\n')  # Add an empty line to separate sentences

                    for i, word_info in enumerate(sentence):
                        prev_word_info = sentence[i - 1] if i > 0 else None
                        prev_2_word_info = sentence[i - 2] if i > 1 else None
                        next_word_info = sentence[i + 1] if i < len(sentence) - 1 else None
                        next_2_word_info = sentence[i + 2] if i < len(sentence) - 2 else None

                        features = extract_features(word_info, prev_word_info, prev_2_word_info, next_word_info, next_2_word_info)
                        out_f.write('\t'.join(features) + '\n')

                sentence = []  # Reset the sentence
                prev_word_info, prev_2_word_info = None, None
            else:
                parts = line.split('\t')
                if len(parts) >= 2:
                    word_info = (parts[0], parts[1])
                    sentence.append(word_info)

# Create the feature files
create_feature_file(train_file, train_feature_file)
create_feature_file(test_file, test_feature_file)
