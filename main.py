import sys
import nltk

def main(request):
    """Given a english phrase, converts it into the appropriate AutoHotkey script"""
    # Determine what kind of script the request is asking for
    # Parse the relevant information out of the request and pass it to function
    return


def launch_app(key, modifier, app_name):
    # Prompt user for full file path
    return


def rebind_key(old_key, modifier, new_key):
    script = mod_to_key(modifier) + old_key + "::\n" + new_key + "\nreturn"
    return


def rebind_phrase(old_phrase, new_phrase):
    script = "::" + old_phrase + "::" + new_phrase
    return script


def mod_to_key(modifier):
    if modifier == "windows":
        return "#"
    elif modifier == "alt":
        return "!"
    elif modifier == "control":
        return "^"
    elif modifier == "shift":
        return "+"
    else:
        return "no_mod_found"

if __name__ == "__main__":
    main(sys.argv[1])
