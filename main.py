import sys
import random
from NER_classifier import *
from nltk.chunk.util import conlltags2tree
from nltk import pos_tag, word_tokenize


def main():
    """Given a english phrase, converts it into the appropriate AutoHotkey script"""
    # Determine what kind of script the request is asking for
    # Parse the relevant information out of the request and pass it to function
    reader = read_gmb("key_remap.tags")
    data = list(reader)
    random.shuffle(data)
    acc = 0
    cross_val = False

    if cross_val:
        for i in range(10):
            if i == 0:
                training_samples = data[int(len(data) * (i + 1) / 10) + 1:]
            elif i == 9:
                training_samples = data[:int(len(data) * i / 10) - 1]
            else:
                training_samples = data[:int(len(data) * i / 10) - 1] + data[int(len(data) * (i + 1) / 10) + 1:]
            test_samples = data[int(len(data) * i / 10):int(len(data) * (i + 1) / 10)]
            chunker = NamedEntityChunker(training_samples)
            score = chunker.evaluate([conlltags2tree([(w, t, iob) for (w, t), iob in iobs]) for iobs in test_samples])
            print(score)
            acc += score._tags_correct / score._tags_total
        print("\n" + "Overall accuracy: {0:.2f}%".format(acc * 10))

    else:
        training_samples = data[:int(len(data) * 0.9) - 1]
        test_samples = data[int(len(data) * 0.9):]
        chunker = NamedEntityChunker(training_samples)
        for iobs in test_samples:
            print(chunker.parse([(word, pos) for (word, pos), iob in iobs]))

    return


def launch_site(key, modifier, site):
    script = mod_to_char(modifier) + key + "::Run " + site
    return script


def launch_app(key, modifier, app_name):
    # Prompt user for full file path
    file_path = ""
    script = mod_to_char(modifier) + key + "::Run " + file_path
    return script


def rebind_key(old_key, modifier, new_key):
    if modifier:
        print("The following script will bind {} + {} to {}".format(modifier, old_key, new_key))
    else:
        print("The following script will bind {} to {}".format(old_key, new_key))
    print(mod_to_char(modifier) + old_key + "::" + new_key)
    return


def rebind_phrase(old_phrase, new_phrase):
    script = "::" + old_phrase + "::" + new_phrase
    return script


def mod_to_char(modifier):
    if modifier.lower() == "windows":
        return "#"
    elif modifier.lower() == "alt":
        return "!"
    elif modifier.lower() == "control":
        return "^"
    elif modifier.lower() == "shift":
        return "+"
    else:
        return ""

if __name__ == "__main__":
    main() #sys.argv[1])
