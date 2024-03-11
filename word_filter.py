import pandas as pd

all = pd.read_csv('data/dictionary.csv', index_col=0)

# keep only 5-letter words without hyphens:
wordle_df = all[all.word.str.contains('^[a-z|A-Z]{5}$', regex=True, na=False)]

# drop duplicate words (keep onyl first occurence)
wordle_df = wordle_df.drop_duplicates(subset='word', keep='first')

# write filtered dictionary to csv
wordle_df.to_csv('data/wordle_dictionary.csv', index=False)