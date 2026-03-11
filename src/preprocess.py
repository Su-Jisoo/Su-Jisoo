# src/preprocess.py
import pandas as pd
import requests
from io import StringIO
from datetime import datetime, timedelta
import numpy as np

URL = "https://www.cwl.gov.cn/cwl_admin/kjxx/findDrawNotice?name=ssq&issueCount=1000"


def fetch_data():
    """
    自动抓取双色球历史数据，返回 DataFrame
    """
    resp = requests.get(URL)
    resp.raise_for_status()
    data = resp.json()["result"]


    rows = []
    for item in data:
        # 抓取期号、开奖日期、红球、蓝球
        issue = int(item["issue"])  # 期号
        date = item["date"]  # 日期 2026-03-10
        red_balls = [int(n) for n in item["red"].split(",")]
        blue_ball = int(item["blue"])
        rows.append([issue, date, *red_balls, blue_ball])

    df = pd.DataFrame(
        rows,
        columns=["issue", "date", "red1", "red2", "red3", "red4", "red5", "red6", "blue"]
    )
    return df


def load_data():
    """
    如果本地有缓存可以读取，否则抓取
    """
    try:
        df = pd.read_csv("data/ssq_history.csv")
        df[["red1", "red2", "red3", "red4", "red5", "red6", "blue"]] = df[
            ["red1", "red2", "red3", "red4", "red5", "red6", "blue"]].astype(int)
    except:
        df = fetch_data()
        df.to_csv("data/ssq_history.csv", index=False)
    return df

def get_latest_issue(df):
    """
    返回最新一期标识，如果没有 issue 列，就用 date 列
    """
    if "issue" in df.columns:
        return df.iloc[-1]["issue"]
    elif "date" in df.columns:
        # 返回日期字符串，例如 '2026-03-10'
        return df.iloc[-1]["date"]
    else:
        raise ValueError("DataFrame中没有 'issue' 或 'date' 列")

def next_issue(latest_issue):
    """
    根据最新期号计算下一期预测期号
    """
    year = str(latest_issue)[:4]
    num = int(str(latest_issue)[4:]) + 1
    return int(f"{year}{num:03d}")


def hot_cold_analysis(df, window=100):
    """
    统计热门和冷门号码
    """
    recent = df.tail(window)
    reds = []
    for _, row in recent.iterrows():
        reds.extend([row["red1"], row["red2"], row["red3"], row["red4"], row["red5"], row["red6"]])
    freq = pd.Series(reds).value_counts()
    hot = freq.head(10)
    cold = freq.tail(10)
    return hot, cold


def omission_analysis(df):
    """
    统计红球遗漏值
    """
    last_seen = {i: 0 for i in range(1, 34)}
    for _, row in df.iterrows():
        reds = [row["red1"], row["red2"], row["red3"], row["red4"], row["red5"], row["red6"]]
        for k in last_seen:
            last_seen[k] += 1
        for r in reds:
            last_seen[r] = 0
    return last_seen


def generate_ai_numbers(prob=None):
    """
    AI简单选号
    """
    if prob is None:
        prob = np.ones(33) / 33
    reds = np.random.choice(np.arange(1, 34), 6, replace=False, p=prob)
    reds.sort()
    blue = np.random.randint(1, 17)
    return reds.tolist(), blue