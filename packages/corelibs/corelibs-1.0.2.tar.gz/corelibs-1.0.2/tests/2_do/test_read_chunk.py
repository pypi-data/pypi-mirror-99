import itertools
import multiprocessing as mp
import re
import sys
from itertools import islice

import unicodedata


def process_chunk(_):
    print(_)


if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count()-4)
    file_path = r"D:\OneDrive\Documents\_TEST_\_bin_.txt"
    with open(file_path) as f:
        while True:
            jobs = []
            chunked_lines = list(islice(f, 6))
            if not chunked_lines:
                break

            for line in chunked_lines:
                results = [pool.apply(process_chunk, x) for x in line]
                # jobs.append(pool.map(process_chunk, line))

            # for job in jobs:
            #     job.get()

            # for line in chunked_lines:
            #     results = pool.map(process_chunk, line)
            #     for r in results:
            #         print(r)

    pool.close()

    control_chars = \
        "".join(c for c in (chr(i) for i in range(sys.maxunicode)) if unicodedata.category(c) in ["Cc"]) \
        .join(map(chr, itertools.chain(range(0x00, 0x20), range(0x7f, 0xa0))))
    re = "[%s]" % re.escape(control_chars)
    print(re)
