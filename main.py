import sys
# import nltk


def main(request):
    """Given a english phrase, converts it into the appropriate AutoHotkey script"""
    # Determine what kind of script the request is asking for
    # Parse the relevant information out of the request and pass it to function
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
    script = mod_to_char(modifier) + old_key + "::" + new_key
    return script


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
    main(sys.argv[1])
