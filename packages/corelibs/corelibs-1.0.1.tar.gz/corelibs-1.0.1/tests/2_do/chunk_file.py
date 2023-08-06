# https://gist.github.com/ngcrawford/2237170
import multiprocessing
from itertools import zip_longest
from textwrap import dedent


def process_chunk(d):
    d = d.strip() + " processed"
    return d


def grouper(n, iterable, padvalue=None):
    return zip_longest(*[iter(iterable)] * n, fillvalue=padvalue)


if __name__ == '__main__':

    # test data
    test_data = """\
1 some test garbage
2 some test garbage
3 some test garbage
4 some test garbage
5 some test garbage
6 some test garbage
7 some test garbage
8 some test garbage
9 some test garbage
10 some test garbage
11 some test garbage
12 some test garbage
13 some test garbage
14 some test garbage
15 some test garbage
16 some test garbage
17 some test garbage
18 some test garbage
19 some test garbage
20 some test garbage
    """
    test_data = dedent(test_data)
    test_data = test_data.split("\n")

    # Create pool (p)
    p = multiprocessing.Pool(4)

    # Use 'grouper' to split test data into
    # groups you can process without using a
    # ton of RAM. You'll probably want to
    # increase the chunk size considerably
    # to something like 1000 lines per core.

    # The idea is that you replace 'test_data'
    # with a file-handle
    # e.g., testdata = open(file.txt,'rU')

    # And, you'd write to a file instead of
    # printing to the stout

    for i, chunk in enumerate(grouper(5, test_data)):
        # print(i, chunk)
        if i < 4:
            results = p.map(process_chunk, chunk)
            for r in results:
                print(r)
