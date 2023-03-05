from bs4 import BeautifulSoup
import glob
import itertools
import os
import re
import requests


def tokenize(text):
    """
    Tokenizes a string of text by splitting on whitespace and removing punctuation.

    Args:
        text: A string of text to be tokenized.

    Returns:
        A list of tokens.
    """
    tokens = re.findall(r'\b\w+\b', text.lower())
    return tokens


def ngrams(tokens, n):
    """
    Generates n-grams from a list of tokens.

    Args:
        tokens: A list of tokens to generate n-grams from.
        n: The number of tokens per n-gram.

    Returns:
        A list of n-grams.
    """
    list_ngrams = []
    for i in range(len(tokens) - n + 1):
        ngram = ' '.join(tokens[i:i + n])
        list_ngrams.append(ngram)
    return list_ngrams


def compare_files(file1, file2, n=3, threshold=0.5):
    """
    Compares two text files for similarity using n-grams.

    Args:
        file1: The path to the first file to be compared.
        file2: The path to the second file to be compared.
        n: The number of tokens per n-gram (default 3).
        threshold: The minimum similarity score for a match (default 0.5).

    Returns:
        A tuple containing the similarity score and a list of matching n-grams.
    """
    # Read in the contents of the files
    with open(file1, 'r') as f1:
        text1 = f1.read()
    with open(file2, 'r') as f2:
        text2 = f2.read()

    # Tokenize the text and generate n-grams
    tokens1 = tokenize(text1)
    tokens2 = tokenize(text2)
    ngrams1 = ngrams(tokens1, n)
    ngrams2 = ngrams(tokens2, n)

    # Calculate the Jaccard similarity coefficient
    intersection = len(set(ngrams1) & set(ngrams2))
    union = len(set(ngrams1) | set(ngrams2))
    similarity = intersection / union

    # Identify matching n-grams
    matches = [ngram for ngram in ngrams1 if ngram in ngrams2]

    # Return the similarity score and matching n-grams
    if similarity >= threshold:
        return similarity, matches
    else:
        return 0, []


def compare_directory(directory, n=3, threshold=0.5):
    """
    Compares all pairs of files in a directory for similarity using n-grams.

    Args:
        directory: The path to the directory containing the files to be compared.
        n: The number of tokens per n-gram (default 3).
        threshold: The minimum similarity score for a match (default 0.5).

    Returns:
        A list of tuples, each containing the paths of two matching files and the similarity score.
    """
    # Get a list of all files in the directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    # Generate all pairs of files
    pairs = itertools.combinations(files, 2)

    # Compare each pair of files for similarity
    matches = []
    for file1, file2 in pairs:
        path1 = os.path.join(directory, file1)
        path2 = os.path.join(directory, file2)
        similarity, _ = compare_files(path1, path2, n, threshold)
        if similarity >= threshold:
            matches.append((path1, path2, similarity))

        return matches


def download_files(keyword, extension="py"):
    """
    Searches the web for files containing the given keyword and downloads the top num_files results.

    Args:
        keyword: A string containing the keyword to search for.
        extension: A string containing the extension of the files desired for download.

    Returns:
        A list of file paths for the downloaded files.
    """
    # Define the query and the URL to search
    # TODO: Make this work for multiple extensions (txt, pdf, docx, etc)
    search_url = f'https://www.google.com/search?q={keyword} filetype:{extension}'

    # Send the search request and parse the HTML using BeautifulSoup
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract links to the files from the search results
    file_links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if ('/url?q=' in href) and ('.' + extension in href):
            url = href.replace('/url?q=', '').split("&sa=")[0]
            if url.endswith('.' + extension):
                file_links.append(url)

    # Download each file and save it to a local directory
    output_dir = 'downloaded_files'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    c = 0
    for link in file_links:
        response = requests.get(link)
        filename = os.path.basename(link)
        output_path = os.path.join(output_dir, filename)
        if os.path.exists(output_path):
            output_path = output_path.replace('.' + extension, '_' + str(c) + '.' + extension)
            c += 1
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f'Downloaded {filename}')

    file_paths = glob.glob(os.path.join(output_dir, "*"))
    return file_paths


my_file = r"C:\Users\gmful\Downloads\threaded_fibonacci.c"

web_files = download_files("ThreadedFibonacci", "c")

for file in web_files:
    similaritysss, matchesss = compare_files(my_file, file, n=3, threshold=0.5)

    if similaritysss >= 0.5:
        print(f'The files are {similaritysss:.2%} similar.')
        print('Matching n-grams:')
        for match in matchesss:
            print(f'- {match}')
    else:  # TODO: Double check, always outputs 0.00% similarity
        print(f'The file {file} is not similar ({similaritysss:.2%}).')
