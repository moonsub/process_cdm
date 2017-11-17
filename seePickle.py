import sys
import cPickle as pickle
import operator
if __name__ == '__main__':
    file = sys.argv[1]
    f = open(file, 'rb')
    a = pickle.load(f)
    print a
    print len(a)
    f.close()
    