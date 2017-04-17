import random
import tkinter as tk
from tkinter import filedialog
from NER_classifier import *
from nltk.chunk.util import conlltags2tree
from nltk import pos_tag, word_tokenize
import script_type_classifier


def main():
    """Given a english phrase, converts it into the appropriate AutoHotkey script"""
    # Determine what kind of script the request is asking for
    # Parse the relevant information out of the request and pass it to function
    evaluate = True
    interactive = False
    script_classifier = script_type_classifier.script_classifier("examples\script_type_examples.txt")

    if evaluate:
        cross_val("examples\key_remap.tags")
        cross_val("examples\launch_website.tags")
        cross_val("examples\launch_app.tags")
        script_classifier.evaluate_gnb()

    if interactive:
        print("Currently supports key remapping, application launching, and website launching.")

        key_chunker = learn_chunker("examples\key_remap.tags")
        site_chunker = learn_chunker("examples\launch_website.tags")
        app_chunker = learn_chunker("examples\launch_app.tags")
        script_gnb = script_classifier.learn_gnb()

        script_request = ""
        while script_request != 'q':
            script_request = input('Enter your script request (q to quit): ')
            if script_request == 'q':
                break
            script_type = script_classifier.predict_script_type(script_gnb, script_request)
            script_type = script_type[0].strip()

            if script_type == 'key':
                parsed_script = key_chunker.parse(pos_tag(word_tokenize(script_request)))
                print(parsed_script)
            elif script_type == 'site':
                parsed_script = site_chunker.parse(pos_tag(word_tokenize(script_request)))
                print(parsed_script)
            elif script_type == 'app':
                parsed_script = app_chunker.parse(pos_tag(word_tokenize(script_request)))
                print(parsed_script)

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


def launch_site(key, modifier, site):
    """Print a script for launching a website"""
    if modifier:
        print("The following script will launch the site {} when you press {} + {}".format(site, modifier, key))
    else:
        print("The following script will launch the site {} when you press {}".format(site, key))
    print(mod_to_char(modifier) + key + "::Run " + site)
    return


def launch_app(key, modifier, app_name):
    """Print a script launching an application"""
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
    """Print a script for rebinding keys"""
    if modifier:
        print("The following script will bind {} + {} to {}".format(modifier, old_key, new_key))
    else:
        print("The following script will bind {} to {}".format(old_key, new_key))
    print(mod_to_char(modifier) + old_key + "::" + new_key)
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
