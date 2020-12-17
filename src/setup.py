# -*- coding: utf-8 -*-
'''
Created on 2017. 5. 9.

@author: Lilie
'''

import configparser
import sys
import os
import inspect

def default(self_dir):
    config = configparser.ConfigParser()
    config.read(self_dir + '/setup.ini')
    return config;

def rewrite(config, section, option, value):    
    self_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    config.set(section, option, value)
    with open(self_dir + '/setup.ini', 'w') as config_set:
        config.write(config_set)
    print('Configuration Changed.')
    setup()
    #return 'rewrite'

def option_select(config, section, select):
    options_list = config.options(section[(int(select) - 1)])
    options_size = len(options_list)
    options_enable = []
    print('[' + section[(int(select) - 1)] + ']')
    for i in range(len(config.options(section[(int(select) - 1)]))):
        print(str(i + 1) + '. ' + options_list[i])
        options_enable.append(str(i + 1))
    options_enable.append(str(options_size + 1))
    options_enable.append(str(options_size + 2))
    print(str(options_size + 1) + '. Section select')
    print(str(options_size + 2) + '. exit')
    

    while True:
        frag = 0
        select_o = input('Select config option number: ')
        if select_o != '':
            for l in options_enable:
                if select_o in l:
                    frag = 1
                    break
            if frag == 1:
                if select_o == str(options_size + 1):
                    setup()
                    break
                elif select_o == str(options_size + 2):
                    sys.exit(0)
                else:
                    option_detail(config, select, select_o)
                    break

def option_detail(config, section, select):
    section_list = config.sections()
    section_name = section_list[int(section) - 1]
    option_list = config.options(section_name)
    option_name = option_list[int(select) - 1]
    option_value = config.get(section_name, option_name)
    print('[' + section_name + ']')
    print('selected option : ' + option_name + '=' + option_value)
    if option_name == 'mailtype':
        print('mailtype only file or text enable.')
    while True:
        print('Option Change. if you exit progrqm insert \'exit\'')
        entered = input('Please Insert Option Value :')
        if entered != '':
            if entered == 'exit':
                setup()
                sys.exit(0)
            else:
                if option_name == 'mailtype':
                    if entered == 'file' or entered == 'text':
                        rewrite(config, section_name, option_name, entered)
                        break
                        
                else:
                    rewrite(config, section_name, option_name, entered)
                    break

def setup():
    self_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    config = default(self_dir)
    section_list = config.sections()
    section_size = len(section_list)
    input_enable = []
    
    print('Section')
    
    for i in range(section_size):
        print(str(i + 1) + '. ' + section_list[i])
        input_enable.append(str(i + 1))
        
    print(str(section_size + 1) + '. exit')
    
    input_enable.append(str(section_size + 1))

    while True:
        frag = 0
        select = input('Select config section number: ')
        if select != '':
            for l in input_enable:
                if select in l:
                    frag = 1
                    break
            if frag == 1:
                if select == str(section_size + 1):
                    sys.exit(0)
                else:
                    option_select(config, section_list, select)
                    break
        
if __name__ == '__main__':
    setup()
