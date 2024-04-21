from configparser import ConfigParser

#Get the configparser object
config_object = ConfigParser()

config_object["settings"] = {
    "subject": "0",
    "random_pick": "True",
    "textbook": "True",
    "midterm": "True",
    "examples": "True"
}

#Write the above sections to config.ini file
#with open('config.ini', 'w') as conf:
#    config_object.write(conf)

from write_config import write_conf, read_conf

list = []
write_conf(0,True,True,False,False)
list = read_conf()
print(list)
