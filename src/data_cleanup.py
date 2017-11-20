import pprint
import os
import json
import copy


current_path = os.path.dirname(__file__)


def preprocess_all_files(directory=None):
    '''
    Function extracts only required data from conllu files
    '''
    # FIXME: loop through all conllu files in the directory
    if directory is None:
        conllu_to_json(current_path + '/../data/en-ud-train.conllu')


def conllu_to_json(filepath=None):
    '''
    converts a conllu file to json
    '''
    # initialize
    text = []

    # Read conllu file
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()

    sentences = source.strip().split('\n\n')

    for sentence in sentences:
        temp_lines = sentence.strip().split('\n')

        sent = {}
        lines = []
        for line in temp_lines:
            words = line.split(' ')
            # Drop all lines beginning with #
            if words[0] == '#':
                if words[1] == 'sent_id':
                    sent['sent_id'] = words[3]
            else:
                lines.append(line)

        words = []
        for line in lines:
            words_list = line.split('\t')
            words.append({
                "id": words_list[0],
                "form": words_list[1],
                "lemma": words_list[2],
                "upostag": words_list[3],
                "xpostag": words_list[4],
                "feats": words_list[5],
                "head": words_list[6],
                "deprel": words_list[7],
                "deps": words_list[8],
                "misc": words_list[9]
            })

        sent['words'] = words
        text.append(sent)

    with open(filepath.replace('.conllu', '.json'), 'w+') as f:
        f.write(json.dumps(text))


if __name__ == '__main__':
    preprocess_all_files()
