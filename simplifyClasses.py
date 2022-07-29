from argparse import ArgumentParser
import glob
import shutil

import numpy as np

my_path = "/workspace/featureData/"
dest = "/workspace/featureDataObject/"
sourceClass = 37


def run(goalClass):
    try:
        shutil.rmtree(dest)
    except Exception as e:
        print('no dir to del')
    shutil.copytree(my_path, dest)

    files = glob.glob(dest + '/**/*.txt', recursive=True)

    for f in files:
        labels = []
        with open(f, mode='rt') as file:
            line: str = file.readline()
            while(line):
                lab = line.split()
                # replace class with 0
                lab[0] = simplifyLabel(lab[0], goalClass)
                labels.append(lab)
                line = file.readline()
        labels = [' '.join(l)+'\n' for l in labels]  # join on whitespace
        with open(f, mode='wt') as file:
            file.writelines(labels)

def simplifyLabel(label, goalClass):
    label = int(label)  # 0-36
    minPersub = sourceClass//goalClass
    rest = sourceClass % goalClass
    distribution = np.ones(goalClass, dtype=np.uint)*minPersub
    if(rest > 0):
        # apply more to the center if uneven rest
        center = np.ceil((goalClass-1)/2) if rest % 2 == 1 else 0
        for i in range(goalClass):
            # alternatig index around ceter pos
            m = np.ceil(i/2)
            m = -m if i % 2 == 1 else m
            distribution[int(center+m)] += 1
            rest = rest-1
            if(rest == 0):
                break
    classs = 0
    for i, count in enumerate(distribution):
        label -= count
        classs = i
        if label < 0:
            break
    widthPerClass = sourceClass/goalClass
    classs = np.round(classs*widthPerClass+widthPerClass/2)
    return str(classs)


if(__name__ == '__main__'):
    parser = ArgumentParser()
    parser.add_argument('count', type=int,
                        help='Number of Class to simplify to')
    args = parser.parse_args()

    print(args)
    run(args.count)
    print('done')
