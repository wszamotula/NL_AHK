import sys
import random
import tkinter as tk
from tkinter import filedialog
from NER_classifier import *
from nltk.chunk.util import conlltags2tree
from nltk import pos_tag, word_tokenize
from script_type_classifier import classify_scripts

def main():
    """Given a english phrase, converts it into the appropriate AutoHotkey script"""
    # Determine what kind of script the request is asking for
    # Parse the relevant information out of the request and pass it to function

    cross_val("examples\key_remap.tags")
    cross_val("examples\launch_website.tags")
    cross_val("examples\launch_app.tags")

    classify_scripts("examples\script_type_examples.txt")

    # reader = read_gmb("key_remap.tags")
    # data = list(reader)
    # random.shuffle(data)
    # training_samples = data[:int(len(data) * 0.9)]
    # test_samples = data[int(len(data) * 0.9):]
    # chunker = NamedEntityChunker(training_samples)
    # for iobs in test_samples:
    #     print(chunker.parse([(word, pos) for (word, pos), iob in iobs]))

    return


def cross_val(tag_file):
    print("\nRunning cross validation score on data set from " + tag_file +":")
    reader = read_gmb(tag_file)
    data = list(reader)
    random.shuffle(data)
    acc = 0
    script_cor = 0
    for i in range(len(data)):
        test_sample = data[i]
        training_samples = data[:]
        del training_samples[i]
        chunker = NamedEntityChunker(training_samples)
        score = chunker.evaluate([conlltags2tree([(w, t, iob) for (w, t), iob in test_sample])])
        # print(score)
        acc += score._tags_correct / score._tags_total
        if score._tags_correct == score._tags_total:
            script_cor += 1
    print("Overall tagging accuracy: {0:.2f}%".format(acc / len(data) * 100))
    print("Percentage of scripts correct: {0:.2f}%".format(script_cor / len(data) * 100))
    return


def launch_site(key, modifier, site):
    if modifier:
        print("The following script will launch the site {} when you press {} + {}".format(site, modifier, key))
    else:
        print("The following script will launch the site {} when you press {}".format(site, key))
    print(mod_to_char(modifier) + key + "::Run " + site)
    return


def launch_app(key, modifier, app_name):
    print("Please select executable for application " + app_name)
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    if modifier:
        print("The following script will launch the app {} when you press {} + {}".format(file_path, modifier, key))
    else:
        print("The following script will launch the app {} when you press {}".format(file_path, key))
    print(mod_to_char(modifier) + key + "::Run " + file_path)
    return


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
