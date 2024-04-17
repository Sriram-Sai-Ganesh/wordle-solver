import pandas as pd

DICTIONARY_FILE = 'data/dictionary.csv'
WORDLE_DICTIONARY_FILE = 'data/wordle_dictionary.csv'

def create_wordle_dictionary(
                    dict_file = DICTIONARY_FILE, 
                    wordle_dict_file = WORDLE_DICTIONARY_FILE
                    ):
    all = pd.read_csv(dict_file, index_col=0)
    # keep only 5-letter words without hyphens:
    wordle_df = all[all.word.str.contains('^[a-z|A-Z]{5}$', regex=True, na=False)]
    # drop duplicate words (keep only first occurence), reset index
    wordle_df = wordle_df.drop_duplicates(subset='word', keep='first').reset_index(drop=True)
    # write filtered dictionary to csv
    wordle_df.to_csv(wordle_dict_file)

def get_wordle_dictionary(wordle_dict_file = WORDLE_DICTIONARY_FILE):
    return pd.read_csv(wordle_dict_file, index_col=0)

def get_dictionary(dict_file = DICTIONARY_FILE):
    return pd.read_csv(dict_file, index_col=0)

def main():
    create_wordle_dictionary()
    
    dictionary = get_dictionary()
    print(f'Full English Dictionary has {len(dictionary)} entries.')
    print(dictionary.head(),'\n')
    
    print(f'Wordle dictionary has {len(get_wordle_dictionary())} entries.')
    wordle_dict = get_wordle_dictionary()
    print(wordle_dict.head())
    
if __name__ == '__main__':
    main()
