# main.py
from src.preprocess import load_data, get_latest_issue, next_issue, hot_cold_analysis, omission_analysis, generate_ai_numbers
import numpy as np

def main():
    df = load_data()
    latest = get_latest_issue(df)
    predict = next_issue(latest)

    print("最新期号或日期：", latest)
    print("预测下一期：", predict)

    hot, cold = hot_cold_analysis(df)
    # print("\n热门号码：")
    # print(hot)
    # print("\n冷门号码：")
    # print(cold)

    omission = omission_analysis(df)
    # print("\n红球遗漏值：")
    # print(omission)

    print("\nAI推荐号码：")
    for i in range(10):
        r, b = generate_ai_numbers()
        red_str = " ".join([f"{x:02d}" for x in r])
        print(f"{i+1}：{red_str} + {b:02d}")

if __name__ == "__main__":
    main()