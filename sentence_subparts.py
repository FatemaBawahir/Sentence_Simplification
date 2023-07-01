import CONSTANTS
import sys
import re

# Assumptions -
# input file has unique sentence id
# input file has - sentence_id - tab separated - sentence
# input file can have many sentences
def log(mssg, logtype='OK'):
    '''Generates log message in predefined format.'''

    # Format for log message
    print(f'[{logtype}] : {mssg}')
    #if logtype == 'ERROR':


def read_input(file_path):
    '''Returns dict with key - sentence_id and value - sentence for data given in file'''

    log(f'File ~ {file_path}')
    try:
        with open(file_path, 'r') as file:
            input_data = {}
            lines = file.readlines()
            for i in range(len(lines)):
                lineContent = lines[i].strip()
                if lineContent == '':
                    break
                else:
                    # sentence_info = lineContent.split('\t')
                    sentence_info = lineContent.split(' ', 1)
                    key = sentence_info[0]
                    value = sentence_info[1].strip()
                    input_data[key] = value
            log('File data read.')
    except FileNotFoundError:
        log('No such File found.', 'ERROR')
        sys.exit()
    return input_data

def validate_sentence(sentence):
    #sentence not empty
    #Regular expression pattern to match any non-digit character
    pattern = r'\D'
    if not len(sentence) or not re.search(pattern, sentence):
        return False

    return True

def write_output(dictionary, file_path):
    with open(file_path, 'w') as file:
        for key, value in dictionary.items():
            line = f"{key}: "
            tuples = [f"({item[0]}, {item[1]})" for item in value]
            line += ', '.join(tuples)
            line += '\n'
            file.write(line)


def generate_simple_sentence(sentence_id, sentence):
    simpler_sentences = []

    # Tokenize the sentence by splitting it into words
    tokens = sentence.split()

    # Iterate through the tokens to find connectives and split the sentence
    current_sentence = []
    current_sentence_id = sentence_id
    for token in tokens:
        # Check if the token is a connective
        if token in CONSTANTS.SIMPLE_CONNECTIVES:
            # Add the current sentence and its ID to the list of simpler sentences
            if len(current_sentence) > 0:
                simpler_sentences.append((" ".join(current_sentence), current_sentence_id))
                current_sentence = []
                current_sentence_id = str(int(current_sentence_id) + 1)
        else:
            # Add the token to the current sentence
            current_sentence.append(token)

        # Add the last sentence and its ID to the list of simpler sentences
    simpler_sentences.append((" ".join(current_sentence), current_sentence_id))

    return simpler_sentences

if __name__ == '__main__':
    input_data = read_input(CONSTANTS.INPUT_FILE)
    output_data = {}
    for key, value in input_data.items():
        if validate_sentence(value):
            sub_sentences = generate_simple_sentence(key, value)
        else:
            sub_sentences = ['Error']

        output_data[key] = sub_sentences

    write_output(output_data, CONSTANTS.OUTPUT_FILE)

