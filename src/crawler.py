import requests
import pandas as pd

URL = "https://datachart.500.com/ssq/history/newinc/history.php?start=03001&end=99999"

def fetch_ssq_data():
    print("开始获取双色球历史数据...")

    tables = pd.read_html(URL)

    df = tables[0]

    df = df.iloc[:, 0:8]

    df.columns = [
        "issue",  # 新增期号列
        "date",
        "red1", "red2", "red3", "red4", "red5", "red6",
        "blue"
    ]

    df = df.dropna()

    df = df[::-1]

    df.to_csv("E:\PythonProject\data\ssq_history.csv", index=False)

    print("数据保存成功")