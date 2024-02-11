Jacob Wang
zw2972

This code is designed to tag noun phrases in a text corpus using Part-of-Speech (POS) tagging and additional features.

## Features

- Noun phrases are tagged based on specific POS patterns.
- Additional features are included:
  - Previous word and POS tag.
  - Next word and POS tag.
  - Previous to previous word and POS tag.
  - Next to next word and POS tag.
  - Capitalization feature (Is_Capitalized) - 0 or 1.
  - Punctuation feature (Is_Punctuation) - 0 or 1.

Input Files

- `train_file`: Path to the training data file (e.g., 'WSJ_02-21.pos-chunk').
- `test_file`: Path to the test data file (e.g., 'WSJ_23.pos').

Output Files

- `train_feature_file`: Path to the output file for training features.
- `test_feature_file`: Path to the output file for test features.
