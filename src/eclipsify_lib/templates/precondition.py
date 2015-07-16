from tools import colored

def fullfilled(config):
    if not config.package:
        print(colored("Package name must not be empty", 'red'))
        return False
    # see end of eclipsify_gen_project.py for how this is called
    return True
