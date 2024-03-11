import re   # URL regex
import bs4  # HTML parsing
import requests # HTTP requests
import pandas as pd # dictionary to CSV
from tqdm import tqdm   # progress through download

# Download the current english dictionary from OPTED
# The Online Plain Text English Dictionary: 
DICT_HOME = 'http://www.mso.anu.edu.au/~ralph/OPTED/'
OUTPUT_DIR = 'data'


# get HTML on page
def get_page_content(url):
    page = requests.get(url)
    return page.content

# write page HTML from url list to output directory
def visit_and_write(urls, output_dir):
    for index, url in enumerate(urls):
        response = requests.get(url).content
        if response.status_code == 200:
            filename = f"{output_dir}/page_{index + 1}.html"
            with open(filename, "w") as file:
                file.write(response.text)
            print(f"Content from {url} written to {filename}")
        else:
            print(f"Failed to retrieve content from {url}")
            
# extract all URLs in an HTML page. 
# Used to get URLs for each letter in the dictionary.
def extract_urls_from_html(html_content):
    # Define the regular expression pattern
    url_pattern = re.compile(r'href=["\'](.*?html*?)["\']', re.IGNORECASE)
    # Find all matches
    urls = url_pattern.findall(html_content)
    return urls

# get absolute URLs for each letter in the dictionary
def get_letter_urls():
    page = get_page_content(DICT_HOME).decode('utf-8')
    letter_urls = [DICT_HOME+single for single in extract_urls_from_html(page)]
    return letter_urls

# read all (word, type, definition) tuples on a single HTLM page
def get_definitions_on_letter_page(url):
    page = get_page_content(url)
    soup = bs4.BeautifulSoup(page, 'html.parser')
    return soup.find_all('p')

# handle splitting of a single data line into word, type, and definition parts.
def handle_definition(single):
    children = list(single.children)
    word = children[0].text
    word_type = children[2].text
    definition = children[-1].text[2:]
    return [word, word_type, definition]


if __name__ == '__main__':
    url_list = get_letter_urls()
    letter_dfs = []
    
    # for each letter URL:
    for letter_url in tqdm(url_list):
        letter_definitions = get_definitions_on_letter_page(letter_url)
        letter_df = pd.DataFrame([handle_definition(single) for single in letter_definitions])
        letter_dfs.append(letter_df)
        
    # concatenate individual letter dfs into a single collective one.
    concat_df = pd.concat(map(pd.DataFrame, letter_dfs), axis=0, ignore_index=True)
    concat_df.columns = ['word', 'type', 'definition']
    
    # write final raw dictionary to CSV.
    concat_df.to_csv('data/dictionary.csv')