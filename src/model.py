import numpy as np


def build_prob(freq):

    numbers = np.arange(1, 34)

    prob = []

    for i in numbers:

        if i in freq:

            prob.append(freq[i])

        else:

            prob.append(0.1)

    prob = np.array(prob)

    prob = prob / prob.sum()

    return numbers, prob


def build_blue_prob(freq):

    numbers = np.arange(1, 17)

    prob = []

    for i in numbers:

        if i in freq:

            prob.append(freq[i])

        else:

            prob.append(0.1)

    prob = np.array(prob)

    prob = prob / prob.sum()

    return numbers, prob