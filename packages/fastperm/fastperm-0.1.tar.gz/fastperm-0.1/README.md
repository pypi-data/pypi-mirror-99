# Overview

Package for online generation of large permutations without a large upfront time or memory cost.

# Installation

    pip install git+https://github.com/adityaramesh/fastperm.git

# Usage

Here is example usage:

    import numpy as np
    from fastperm import Permutation

    rs = np.random.RandomState(seed=0xfeedface)

    for i in Permutation(1_000_000_000, rs):
        # Do something
        pass

Note that generating _all_ elements of the permutation is much slower than `np.random.permutation`, since the algorithm
is implemented in Python. However, the time and memory cost -- both for construction and to generate the next element of
the permutation -- are both O(1). This may make it a better option when very large permutations are required.
