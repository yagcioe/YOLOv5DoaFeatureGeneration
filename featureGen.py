import math
import multiprocessing as mp
import os
from argparse import ArgumentParser

from sklearn.utils import shuffle

from featureExtraction import featurePipe as pipe
from roomgen import generate as gen


def clearDir():
    pipe.clearDir()


def run(count, startId, logger=None):
    g = gen.generate(count, startId)
    it = iter(iterDiv(7, 2, 1))
    for i, (sampleNr, roomWav, wavs, json_data, fig) in enumerate(g):
        if(logger != None):
            nBlocks=25
            perc = i/count
            blocks = math.floor(perc*nBlocks)
            s = '['+'#'*blocks+'-'*(nBlocks-blocks) + \
                f'] {i}/{count}, {math.floor(perc*100)}%' + 10*' '
            logger(s, end='\r') if i<count else logger(s)
        img, lab, id = pipe.transform(roomWav, json_data)
        pipe.export(img, lab, id, next(it))



def runParallel(samplesPerWorker, workers=os.cpu_count(), startId=1):
    processes = []
    for i in range(workers):
        p = mp.Process(target=run, args=(
            samplesPerWorker, i*samplesPerWorker+startId, print if i == 0 else None))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
    print('')
    print('done')


class iterDiv:
    def __init__(self, tr, va, ts):
        self.arr = []
        for i in range(tr):
            self.arr.append('train/')
        for i in range(va):
            self.arr.append('val/')
        for i in range(ts):
            self.arr.append('test/')
        shuffle(self.arr)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if(self.n == len(self.arr)):
            self.n = 0
        r = self.arr[self.n]
        self.n += 1
        return r


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('count', type=int,
                        help='Number of Samples per CPU core')
    parser.add_argument("--clear", action='store_true', dest='clear',
                        help='removing all previous generated samples')
    parser.add_argument('--start', type=int, default=0,
                        dest='start', help='Starting index of the samples')
    parser.add_argument('--cores', type=int,
                        default=os.cpu_count(), dest='cores', help='cores to use')

    args = parser.parse_args()

    print(args)

    if args.cores > os.cpu_count():
        raise ValueError('Core count cannot exceed '+str(os.cpu_count()))

    if(args.count < 0 or args.start < 0 or args.cores < 0):
        raise ValueError('Arguments cannot be less than 0')

    if(args.clear):
        try:
            clearDir()
        except:
            pass

    if args.cores == 1:
        run(args.count, args.start, print)
    else:
        runParallel(args.count, args.cores, args.start)
