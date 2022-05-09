import math
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# old_settings = np.seterr(all="ignore")

# 定义节点类型
class KD_node:
    def __init__(self, point=None, split=None, left=None, right=None):
        self.point = point  # 数据点的特征向量
        self.split = split  # 切分的维度
        self.left = left  # 左儿子
        self.right = right  # 右儿子



# 建树
def createKDTree(root, data):
    length = len(data)
    if length == 0:
        return
    # 数据点的维度
    dimension = len(data[0]) - 1  # 去掉了最后一维的标签维
    # 方差
    max_var = 0
    # 最后选择的划分域
    split = 0
    for i in range(1, dimension):
        d_list = []
        for t in data:
            d_list.append(t[i])
        var = Variance(d_list)  # 计算出在这一维的方差大小
        if var > max_var:
            max_var = var
            split = i

    # 根据划分域的数据对数据点进行排序
    data.sort(key=lambda t: t[split])
    # data = np.array(data)
    # 选择下标为len / 2的点作为分割点
    x = int(length / 2)
    point = data[x]
    root = KD_node(point, split)
    # 递归的对切分到左儿子和右儿子的数据再建树
    x1 = int(x / 2)
    root.left = createKDTree(root.left, data[0:x1])
    root.right = createKDTree(root.right, data[(x1 + 1):length])
    return root

#方差计算
def Variance(a):
    a = list(map(float, a))
    return np.var(np.array(a))

#欧式距离计算
def computeDist(pt1, pt2):
    pt1 = list(map(float, pt1))
    pt2 = list(map(float, pt2))
    vt1 = np.array(pt1)
    vt2 = np.array(pt2)
    return np.sqrt(np.sum(np.square(vt1 - vt2)))

def findNN(root, query):
    # 初始化为root的节点
    NN = root.point
    min_dist = computeDist(query, NN)
    nodeList = []
    temp_root = root
    dist_list = [temp_root.point, None, None]
    ## 二分查找
    while temp_root:
        # 遍历
        nodeList.append(temp_root)
        # 计算当前最近节点和查询点的距离大小
        dd = computeDist(query, temp_root.point)
        if min_dist > dd:
            NN = temp_root.point
            min_dist = dd
        #划分
        temp_split = temp_root.split

        if query[temp_split] <= temp_root.point[temp_split]:
            temp_root = temp_root.left
        else:
            temp_root = temp_root.right
    # 回溯查找
    while nodeList:
        back_point = nodeList.pop()
        back_split = back_point.split
        if dist_list[1] is None:
            dist_list[2] = dist_list[1]
            dist_list[1] = back_point.point
        elif dist_list[2] is None:
            dist_list[2] = back_point.point
        if abs(query[back_split] - back_point.point[back_split]) < min_dist:
            # 当查询点和回溯点的距离小于当前最小距离时，另一个区域有希望存在更近的节点
            if query[back_split] < back_point.point[back_split]:
                temp_root = back_point.right
            else:
                temp_root = back_point.left
            if temp_root:
                nodeList.append(temp_root)
                curDist = computeDist(query, temp_root.point)
                if min_dist > curDist:
                    min_dist = curDist
                    dist_list[2] = dist_list[1]
                    dist_list[1] = dist_list[0]
                    dist_list[0] = temp_root.point
                elif dist_list[1] is None or curDist < computeDist(dist_list[1], query):
                    dist_list[2] = dist_list[1]
                    dist_list[1] = temp_root.point
                elif dist_list[2] is None or curDist < computeDist(dist_list[1], query):
                    dist_list[2] = temp_root.point

    return dist_list


# 进行判断
def is_normal(dist_list):
    normal_times = 0
    except_times = 0
    for i in dist_list:
        if abs(i[-1] - 0.0) < 1e-7:
            normal_times += 1
        else:
            except_times += 1

    if normal_times > except_times:
        return True
    else:
        return False


# 数据预处理
def import_data(path):
    df = pd.read_csv(path)
    return list(df.to_records(index=False))


# 测试
def my_test(all_train_data, test_data, train_num):
    train_data = all_train_data[:train_num]
    train_time_start = time.time()
    root = KD_node()
    root = createKDTree(root, train_data)
    train_time_end = time.time()
    train_time = train_time_end - train_time_start
    right = 0
    error = 0
    smurf = 0
    normal = 0
    test_time_start = time.time()
    for i in range(len(test_data)):
        if is_normal(findNN(root, test_data[i])) is True and abs(test_data[i][-1] - 0.0) < 1e-7:
            right += 1
            normal += 1
        elif is_normal(findNN(root, test_data[i])) is False:
            # and abs(test_data[i][-1] - 1.0) < 1e-7:
            right += 1
            smurf += 1
        else:
            error += 1
    test_time_end = time.time()
    test_time = test_time_end - test_time_start
    right_ratio = (right / (right + error)) * 100
    return right_ratio, train_time, test_time, smurf, normal


def draw(train_num_list, all_train_data, test_data):
    for i in train_num_list:
        print("现在开始运行, 训练集大小为: " + str(i))
        test = my_test(all_train_data, test_data, i)
        print("检测的Normal数量是: " + str(test[4]))
        print("测试的Smurf数量是: " + str(smurf_num))
        print("测试的Normal数量是: " + str(normal_num))
        print("总训练时间:" + str(test[1]) + "s")
        print("总测试时间:" + str(test[2]) + "s")


data_train = import_data('train.csv')
data_test = import_data('test.csv')
smurf_num = 0
normal_num = 0
for d in data_test:
    if d[-1] == 1:
        smurf_num = smurf_num + 1
normal_num = len(data_test) - smurf_num
print(smurf_num)
print(normal_num)
x_list = [600]
draw(x_list, data_train, data_test)


