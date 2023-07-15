import re
from nltk.corpus import wordnet as wn
import pickle
import os
from get_file import get_file_path

PICKLEPATH = "pickled_list.pickle"
WORDLISTPATH = "word_list.txt" # default file name. user chooses a file when you run the program.
TEXPATH = "out.tex"


def pickle_dict(word_dict):
    # Pickle the list
    pickled_dict = pickle.dumps(word_dict)

    # Save the pickled list to a file
    with open(PICKLEPATH, "wb") as file:
        file.write(pickled_dict)


def unpickle_dict():
    # Load the pickled list from a file
    if os.path.exists(PICKLEPATH):
        with open(PICKLEPATH, "rb") as file:
            pickled_dict = file.read()
        unpickled_dict = pickle.loads(pickled_dict)
    else:
        unpickled_dict = dict()

    return unpickled_dict


def create_dict_entry(word):
    synsets = wn.synsets(word)
    entry = f"\\entry{{{word}}}"
    if synsets:
        entry += '{'
        for synset in synsets:
            definition = synset.definition()
            definition = definition.replace("%", r"\%")
            definition = definition.replace("&", r"\&")
            partOfSpeech = "noun" if synset.pos() == 'n' else "verb" if synset.pos() == 'v' else "adjective" if synset.pos() == 'a' else "adverb" if synset.pos() == 'r' else synset.pos()
            entry += f" (\\textbf{{\\textit{{{partOfSpeech}}}}}): {definition}\\\\"
        entry += '}\n\n'
    else:
        entry += f" {{No definition found.\\\\}}\n\n"
    return entry




def insert(word_dict):
    content = ''
    with open(WORDLISTPATH, 'r') as f:
        for token in f.read().split():
            if token.isdigit():
                content += f'\\section*{{{token}}}\n\n'
            else:
                print(token, "in dictionary:", word_dict[token])
                content += word_dict[token]
    return content




def add_entries(word_dict, word_list):
    for word in word_list:
        word_dict[word] = create_dict_entry(word)
    return word_dict

        
def get_word_list():
    with open(WORDLISTPATH, 'r') as f:
        return [word for word in f.read().split() if not word.isdigit()]


def replace_tex_content():
    with open(TEXPATH, 'r') as f:
        tex_content = f.read()
    new_list = get_word_list()
    last_dict = unpickle_dict()
    new_list = list(set(new_list) - set(last_dict.keys()) )
    new_dict = add_entries(last_dict, new_list)
    print(new_list,"is new list")
    pickle_dict(new_dict)
    new_content = insert(new_dict)
                    

    # Construct the regular expression pattern
    pattern = r"\\begin\{document\}(.*?)\\end\{document\}"

    # Search for the content between \begin{document} and \end{document}
    match = re.search(pattern, tex_content, re.DOTALL)
                    
    if match:
        # Extract the content between the patterns
        extracted_content = match.group(1)


        # Replace the original content with the modified content
        modified_file_content = tex_content.replace(match.group(1), new_content)

        # Write the modified content back to the file
        with open(TEXPATH, 'w') as file:
            file.write(modified_file_content)

        print("New content inserted successfully.")
    else:
        print("No content found between \\begin{" + begin_pattern + "} and \\end{" + end_pattern + "}.")



file_path = get_file_path()
if file_path:
    WORDLISTPATH = file_path
replace_tex_content()

