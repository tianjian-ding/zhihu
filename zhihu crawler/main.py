import getAnswers
import getHotBoard
import time


def main():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 标定当前时间
    print(current_time)
    with open("./logfile.txt","a") as file:

        try:
            getHotBoard.main(current_time)
            print("%s   hot board collected\n"%current_time)
            file.write("%s   hot board collected\n"%current_time)
        except Exception as e:
            print("%s   hot board collect error: %s\n" % (current_time, e))
            file.write("%s   hot board collect error: %s\n" % (current_time, e))

        try:
            getAnswers.main(current_time)
            print("%s   answer collected\n" % current_time)
            file.write("%s   answer collected\n"%current_time)
        except Exception as e:
            print("%s   answer collect error: %s\n" % (current_time, e))
            file.write("%s   answer collect error: %s\n" % (current_time, e))




if __name__ == '__main__':
    while True:

        main()
        time.sleep(3600)