"""CLI script to dump pickle/cache files"""
import sys
import pickle
from pprint import pprint

def main():
    """Read pickle file and pretty print it"""
    with open(sys.argv[1], "rb") as f:
        x = pickle.load(f)
        pprint(x)

if __name__ == '__main__':
    main()
