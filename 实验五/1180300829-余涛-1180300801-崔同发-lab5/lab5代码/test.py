import numpy as np


def process(path):

    f = open(path, "r", encoding="utf8")
    f_train = open("train.csv", "w", encoding="utf8")
    f_test = open("test.csv", "w", encoding="utf8")
    line = f.readline()
    for i in range(10000):
        line = f.readline()
    train_line_number = 0
    test_normal_line_number = 0
    test_smurf_line_number = 0
    train_normal_number=0
    while line:
        split_line = line.split(",")
        label = split_line[41].rstrip(".\n")
        line_write = ""
        for word in split_line[4:40]:
            line_write += word + ","
        line_write.rstrip(",")
        if label == "normal":
            if train_line_number < 1000 and train_normal_number<800:
                train_line_number += 1
                train_normal_number+=1
                f_train.write(line_write + "0\n")
            else:
                if test_normal_line_number < 500:
                    test_normal_line_number += 1
                    f_test.write(line_write  + "0\n")
        elif label == "smurf":
            if train_line_number < 600 and train_normal_number>=400:
                train_line_number += 1
                f_train.write(line_write + "1\n")
            elif test_smurf_line_number < 300:
                test_smurf_line_number += 1
                f_test.write(line_write +  "1\n")
        line = f.readline()
    f.close()
    f_test.close()
    f_train.close()





if __name__ == '__main__':
    process("kddcup.data_10_percent_corrected")


