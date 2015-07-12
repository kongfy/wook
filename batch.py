# -*- coding: utf-8 -*-

import os
import os.path
import shutil

def configs():
    for root, dirs, files in os.walk('configs'):
        for filename in files:
            yield os.path.join(root, filename)

def main():
    config_filename = os.path.join(os.getcwd(), 'config.py')
    config_pyc = config_filename + 'c'
    result_dir = os.path.join(os.getcwd(), 'results')
    for config in configs():
        if os.path.exists(config_pyc):
            os.remove(config_pyc)

        shutil.copy(config, config_filename)

        if not os.path.exists(result_dir):
            os.mkdir(result_dir)

        output = os.path.basename(config)[:os.path.basename(config).rfind('.')] + '.out'
        cmd = 'python main.py > ' + os.path.join(result_dir, output)
        
        print cmd
        os.system(cmd)
        
if __name__ == '__main__':
    main()
        