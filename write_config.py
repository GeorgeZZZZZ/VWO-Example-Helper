from configparser import ConfigParser
import time

def write_conf(sub, rP, tex, midt, examp):
    #Get the configparser object
    config_object = ConfigParser()

    config_object["settings"] = {
        "subject": sub,
        "random_pick": rP,
        "textbook": tex,
        "midterm": midt,
        "examples": examp
    }

    #Write the above sections to config.ini file
    with open('config.ini', 'w') as conf:
        c = config_object.write(conf)

def read_conf():
    config_object = ConfigParser()
    s_v = []
    try:
        config_object.read("config.ini")
        settings = config_object["settings"]
    except:
        return -1
    else:
        settings = config_object["settings"]
        s_v.append(settings["subject"])
        s_v.append(settings["random_pick"])
        s_v.append(settings["textbook"])
        s_v.append(settings["midterm"])
        s_v.append(settings["examples"])
        return s_v