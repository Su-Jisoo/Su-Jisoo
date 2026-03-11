import pandas as pd

def hot_cold_analysis(df, window=100):
    recent = df.tail(window)
    reds = []
    for _, row in recent.iterrows():
        reds.extend([
            row["red1"], row["red2"], row["red3"],
            row["red4"], row["red5"], row["red6"]
        ])
    freq = pd.Series(reds).value_counts()
    hot = freq.head(10)
    cold = freq.tail(10)
    return hot, cold

def omission_analysis(df):

    last_seen = {}

    for i, row in df.iterrows():

        for n in range(1, 34):

            if n not in last_seen:
                last_seen[n] = 0

        reds = [
            row["red1"], row["red2"], row["red3"],
            row["red4"], row["red5"], row["red6"]
        ]

        for n in last_seen:
            last_seen[n] += 1

        for r in reds:
            last_seen[r] = 0

    return last_seen