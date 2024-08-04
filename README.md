# Fine Tune Dataset

## Working with the dataset:
1. Each folder inside the `datasets` directory represents the a type of dataset.
2. Each json file inside the folder represents a data sample.

## Compiling into jsonl file (File names don't matter):
1. If you would like to compile `resume_train` and `resume_val` run `python generate_results.py resume_train resume_val`.
2. The script can handle more than one at once.
3. The datasets need to be in the `datasets` directory.

## If you have a jsonl file and want to seperate:
1. If you have `theory_train.jsonl` run the command `python update_dataset.py theory_train.jsonl`
2. The script expects the file to be placed in the `results` directory.
3. This script will delete existing data from the `datasets/theory_train` directory.
4. It will then create new json files according to the provided file.
5. Line number is used as the file name.

## Atmik
## Training Data
1. Context Setting: 1-11
2. All cases mixed: 12,13
3. Case E(All answers right): 14,15,16
4. Case B,C,D: 17,18
5. Arguement, Break: 19,20,21
6. Negative,Arguement, Case B, Case C: 22-27

# Validation Data
1. Mixed with all cases
2. Context Setting
3. Case E with break
4. Arguement, Case B, Case E
5. Purely Case A
6. Case D, Case C, Case A
7. Case B, Cross question, Hint
8. Case A, B
9. Case B, C, D.
10. Context setting, Hint
11. Case E with context setting
12. Case B,C,D
13. Case C,D
14. Case C,B,D