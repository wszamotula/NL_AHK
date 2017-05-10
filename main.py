import random
import tkinter as tk
from tkinter import filedialog
from NER_classifier import *
from nltk.chunk.util import conlltags2tree
from nltk import pos_tag, word_tokenize
import script_type_classifier
import pickle
import os


def main():
    """Given a english phrase, converts it into the appropriate AutoHotkey script"""
    evaluate = True
    interactive = True
    reload_classifiers = False
    script_classifier = script_type_classifier.script_classifier("examples\script_type_examples.txt")

    if evaluate:
        evaluation_mode(script_classifier)
    if interactive:
        interactive_mode(reload_classifiers, script_classifier)

    return


def evaluation_mode(script_classifier):
    '''Evaluate the accuracy of the named entity taggers and script type classifier using cross validation'''
    script_classifier.evaluate_nb()
    cross_val("examples\key_remap.tags")
    cross_val("examples\launch_website.tags")
    cross_val("examples\launch_app.tags")
    return


def interactive_mode(reload_classifiers, script_classifier):
    '''Present interactive display to user for converting script requests into script code'''
    print("Currently supports key remapping, application launching, and website launching.")
    directory = 'classifiers'

    if reload_classifiers:
        key_chunker = learn_chunker("examples\key_remap.tags")
        site_chunker = learn_chunker("examples\launch_website.tags")
        app_chunker = learn_chunker("examples\launch_app.tags")
        script_nb = script_classifier.learn_nb()
        pickle.dump(key_chunker, open(os.path.join(directory, 'key_chunker'), 'wb'))
        pickle.dump(site_chunker, open(os.path.join(directory, 'site_chunker'), 'wb'))
        pickle.dump(app_chunker, open(os.path.join(directory, 'app_chunker'), 'wb'))
        pickle.dump(script_nb, open(os.path.join(directory, 'script_nb'), 'wb'))
    else:
        key_chunker = pickle.load(open(os.path.join(directory, 'key_chunker'), 'rb'))
        site_chunker = pickle.load(open(os.path.join(directory, 'site_chunker'), 'rb'))
        app_chunker = pickle.load(open(os.path.join(directory, 'app_chunker'), 'rb'))
        script_nb = pickle.load(open(os.path.join(directory, 'script_nb'), 'rb'))

    script_request = ""
    while script_request != 'q':
        script_request = input('\nEnter your script request (q to quit): ')
        if script_request == 'q':
            break
        script_type = script_classifier.predict_script_type(script_nb, script_request)
        script_type = script_type[0].strip()
        tokenized_request = pos_tag(word_tokenize(script_request))

        if script_type == 'key':
            rebind_key(key_chunker.parse(tokenized_request))
        elif script_type == 'site':
            launch_site(site_chunker.parse(tokenized_request))
        elif script_type == 'app':
            launch_app(app_chunker.parse(tokenized_request))

    return


def learn_chunker(tag_file):
    """Learn a NER chunker for a given tag file"""
    reader = read_gmb(tag_file)
    data = list(reader)
    random.shuffle(data)
    return NamedEntityChunker(data)


def cross_val(tag_file):
    """Perform leave one out cross validation for a NER chunker given a tag file"""
    print("\nRunning cross validation score on data set from " + tag_file + ":")
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
        acc += score._tags_correct / score._tags_total
        if score._tags_correct == score._tags_total:
            script_cor += 1
    print("Overall tagging accuracy: {0:.2f}%".format(acc / len(data) * 100))
    print("Percentage of scripts correct: {0:.2f}%".format(script_cor / len(data) * 100))
    return


def launch_site(parsed_script):
    """Print a script for launching a website"""
    key = ""
    modifier = ""
    site = ""

    for token in parsed_script:
        if hasattr(token, '_label'):
            if token._label == 'site':
                site += token[0][0]
            elif token._label == 'mod':
                modifier += token[0][0]
            elif token._label == 'key':
                key += token[0][0]

    if modifier:
        print("\tThe following script will launch the site {} when you press {} + {}".format(site, modifier, key))
    else:
        print("\tThe following script will launch the site {} when you press {}".format(site, key))
    print('\t' + mod_to_char(modifier) + key + "::Run " + site)
    return


def launch_app(parsed_script):
    """Print a script launching an application"""
    key = ''
    modifier = ''
    app_name = ''

    for token in parsed_script:
        if hasattr(token, '_label'):
            if token._label == 'app':
                app_name += token[0][0]
            elif token._label == 'mod':
                modifier += token[0][0]
            elif token._label == 'key':
                key += token[0][0]

    print("\tPlease select executable for application " + app_name)
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    if modifier:
        print("\tThe following script will launch the app {} when you press {} + {}".format(app_name, modifier, key))
    else:
        print("\tThe following script will launch the app {} when you press {}".format(app_name, key))
    print('\t' + mod_to_char(modifier) + key + "::Run " + file_path)
    return


def rebind_key(parsed_script):
    """Print a script for rebinding keys"""
    old_key = ''
    modifier = ''
    new_key = ''

    for token in parsed_script:
        if hasattr(token, '_label'):
            if token._label == 'orig':
                old_key += token[0][0]
            elif token._label == 'mod':
                modifier += token[0][0]
            elif token._label == 'repl':
                new_key += token[0][0]

    if modifier:
        print("\tThe following script will bind {} + {} to {}".format(modifier, old_key, new_key))
    else:
        print("\tThe following script will bind {} to {}".format(old_key, new_key))
    print('\t' + mod_to_char(modifier) + old_key + "::" + new_key)
    return


# def rebind_phrase(old_phrase, new_phrase):
#     script = "::" + old_phrase + "::" + new_phrase
#     return script


def mod_to_char(modifier):
    """return the AHK code for a given modifier"""
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
    main()  # sys.argv[1])
