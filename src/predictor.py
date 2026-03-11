import numpy as np

def generate_ai_numbers(prob):

    nums = np.arange(1, 34)

    reds = np.random.choice(
        nums,
        6,
        replace=False,
        p=prob
    )

    reds = sorted(reds)

    blue = np.random.randint(1,17)

    return reds, blue