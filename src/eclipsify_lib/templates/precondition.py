from tools import colored

def fullfilled(config):
    # see end of eclipsify_gen_project.py for how this is called
    if not config.package:
        print(colored("Package name must not be empty", 'red'))
        return False
    return True
