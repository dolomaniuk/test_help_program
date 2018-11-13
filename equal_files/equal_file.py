import os

path = input('Enter path with files\n')


def find_file(find_file):
    list = []
    for rootdir, dirs, files in os.walk(path):
        for file in files:
            list.append(file.__str__().split())
    if not (find_file.split() in list):
        print(find_file)


with open('list.txt', 'r') as list_files:
    for line in list_files:
        find_file(line)
