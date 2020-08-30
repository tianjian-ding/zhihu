import getHotBoard
import getAnswers
import time


def main():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 标定当前时间
    print(current_time)
    try:
        getHotBoard.main(current_time)
        print("hot board collected")
    except Exception as e:
        print("hot board error")
        print(e)

    try:
        getAnswers(current_time)
        print("answers collected")
    except Exception as e:
        print("answers error")
        print(e)