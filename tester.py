import subprocess
import os
from glob import glob

def main():
    script_location = os.getcwd()
    folder_name = 'trainall/'
    files = glob(script_location + '/' + folder_name + '*')
    files = ['trainall/test_M.wav', 'trainall/test_K.wav']
    files = ['001_K.wav']
    counter = 0
    for file in files:
        name = os.path.splitext(os.path.basename(file))
        path = folder_name + name[0] + name[1]
        test = 1 if name[0][-1] == 'M' else 0
        process = subprocess.call(['python3', 'gender_recognition.py', path])
        counter = counter + (process == test)
    print('correct files:', counter)
    print('all files count: ', len(files))

if __name__ == '__main__':
    main()
