# 读入文法
from collections import defaultdict
from texttable import Texttable
import pandas as pd

global f

#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows',None)

pd.set_option('display.width', 5000)





gramma = open("gramma.txt", 'r', encoding='UTF-8')

# 读入终结符和非终结符
# vt:终结符
# vn:非终结符
vt = open('vt.txt', 'r', encoding='UTF-8').readline().split(' ')
vn = open('vn.txt', 'r', encoding='UTF-8').readline().split(' ')

startCode = vn[0]


# vt = ['id','(',')','+','*','epsilon','#']
# vn = ['E','T',"E'","T'",'F']


# 建立一个栈
class Stack(object):
    def __init__(self):
        self.__list = []

    def push(self, item):
        self.__list.append(item)

    def pop(self):
        return self.__list.pop()

    def top(self):
        if self.__list:
            return self.__list[-1]
        return None

    def is_empty(self):
        return self.__list == []

    def size(self):
        return len(self.__list)

    def show(self):
        return ''.join(self.__list)


# ————————————————
# 其中，查找非终结符的First集步骤为：
# Step 1. 按产生式顺序来，从开始符找起；
# Step 2. 如果右部的串首为终结符，则直接将该终结符填入左部非终结符的First集中；
# Step 3. 如果右部的串首为非终结符，则左部非终结符的First集等价于串首非终结符的First集。
# 		因而，需要利用Step 2和Step 3继续寻找串首非终结符的First集。
#
# 查找非终结符的Follow集步骤为：
# Step 1. 按产生式顺序来，从开始符找起（开始符的Follow集必定包含`#`）；
# Step 2. 从所有产生式右部寻找目标非终结符，若其后紧跟终结符，则将终结符填入目标非终结符的
# 		Follow集。特别地，若其后紧跟`#`，则目标非终结符的Follow集等价于产生式左部非终结符
# 		的Follow集。
# Step 3. 从所有产生式右部寻找目标非终结符，若其后紧跟非终结符，则将该非终结符的First集元素
# 		填入目标非终结符的Follow集。特别地，若该非终结符的First集元素中包含#\epsilon#，
# 		则需针对#\epsilon#情况时做特殊处理，即目标非终结符的Follow集等价于产生式左部
# 		非终结符的Follow集。
# ————————————————


# 把文法中A->B|C 切分为A->B和A->C
def splitOr(gramma):
    stack = []
    for i in gramma:
        i = i.split(' ')
        ss = i[0]
        j = 1
        while j < len(i):
            if i[j] == "->":
                break
            j += 1
        j += 1
        while j < len(i):
            if i[j][-1] == '\n':
                i[j] = i[j][0:-1]
            if i[j] != '|':
                ss += " " + i[j]
            else:
                stack.append(ss.split(' '))
                ss = i[0]
            j += 1
        stack.append(ss.split(' '))
    return stack


productions = splitOr(gramma)



repr(productions)
strG = ""
for aG in productions:
    strG += aG[0]
    strG += " -> "
    for w in aG[1:]:
        strG += w + " "
    strG += "\n"

# print(strG)
f3 = open("out3.txt", 'w+', encoding='UTF-8')

f3.write(strG)
f3.write("\n\n")


# 创建First和Follow集
first = defaultdict(set)
follow = defaultdict(set)


def getFirst(curVn):
    # 这里是为了下面递归搜索的时候以免已经确定的first再进行一次计算，下面的getFollow函数同。
    # 只要集合不为空说明已经求过则可以直接返回值即可。
    if first[curVn] != set():
        return first[curVn]
    # print(curVi)
    # 遍历每个产生式，找到左边是我们需要求的非终结符的产生式。
    for curPro in productions:
        if curPro[0] == curVn:
            # print(" ",curPro)
            # 判断右侧首字符是否为终结符。
            if curPro[1] in vt:
                first[curVn].add(curPro[1])
            else:
                # 加入最开始的递归直接返回判断后，这里其实不需要if语句。
                # 唯一这样做可能会省去部分递归过程，节省一点点系统栈空间。
                if first[curPro[1]] == set():
                    first[curVn] = set(getFirst(curPro[1]))
                else:
                    first[curVn] = set(first[curPro[1]])
    return first[curVn]


def getFollow(curVn):
    # 同上
    if curVn != 'E' and follow[curVn] != set():
        # print(1)
        return follow[curVn]
    # print(curVn)
    # 这两层循环是为了在产生式右侧找到正在求的非终结符
    for curPro in productions:
        l = len(curPro)
        for i in range(1, l):
            if curPro[i] != curVn:
                continue
            # print(curPro)
            # 如果当前非终结符是列表最后一个元素那么他的下一个元素一定是结束符#
            if i == l - 1:
                # print(2)
                follow[curVn] = set(getFollow(curPro[0]))
                follow[curVn].add('#')
                continue
            # 判断后面的是终结符还是非终结符
            if curPro[i + 1] in vt:
                # print(3)
                follow[curVn].add(curPro[i + 1])
            elif curPro[i + 1] in vn:
                # 下面的这个if-eles其实能简化，需要的自己简化去吧。
                if 'epsilon' in first[curPro[i + 1]]:
                    # print(4)
                    follow[curVn] = follow[curVn] | first[curPro[i + 1]]
                    follow[curVn] = follow[curVn] | set(getFollow(curPro[0]))
                    follow[curVn].discard('epsilon')
                else:
                    # print(5)
                    follow[curVn] = follow[curVn] | first[curPro[i + 1]]
    return follow[curVn]


# 对于每一个非终结符求first集合和follow集合
for aVn in vn:
    getFirst(aVn)

follow[startCode].add('#')
for aVn in vn:
    getFollow(aVn)

str1 = "First:\n"
for key in first.keys():
    # print(first[key])
    str1 += key
    str1 += ": "
    str1 += str(first[key]) + "\n"
str1 += "\nFollow:\n"
for key in follow.keys():
    str1 += key
    str1 += ": "
    str1 += str(follow[key]) + "\n"

f3.write(str1)
f3.write("\n\n")

# 对一个串求First集
dirFirst = defaultdict(set)


def getDirFirst(curPro):
    res = []
    # 对于一个字符串求first集
    for i in range(1, len(curPro)):
        if curPro[i] in vt:
            res.append(curPro[i])
            break
        elif curPro[i] in vn:
            if 'epsilon' in first[curPro[i]]:
                res.extend(first[curPro[i]])
            else:
                res.extend(first[curPro[i]])
                break
    # 去重
    ress = []
    for i in res:
        if i not in ress:
            ress.append(i)
    return ress


# 生成dataForm的格式
dfData = [[[] for i in range(len(vt))] for i in range(len(vn))]
dfData1 = [["" for i in range(len(vt))] for i in range(len(vn))]

M = pd.DataFrame(data=dfData, index=vn, columns=vt)
outM = pd.DataFrame(data=dfData1, index=vn, columns=vt)

# print(outM)

# print(M)
# print(M.loc['E']['+'])
def getM():
    # step1



    for curPro in productions:
        A = curPro[0]
        dirFirst = getDirFirst(curPro)
        # print(A)
        # print(dirFirst)
        for a in dirFirst:
            if a == 'epsilon':
                continue
            strForm = curPro[0] + "->"
            for w in curPro[1:]:
                strForm += w
            M.loc[A][a].append(curPro)
            outM.loc[A][a] += "    " + strForm
    # step2
    for curPro in productions:
        A = curPro[0]
        dirFirst = getDirFirst(curPro)
        # print(curPro)
        # print(' ',dirFirst)
        if 'epsilon' in dirFirst:
            for b in follow[A]:
                strForm = curPro[0] + "->"
                for w in curPro[1:]:
                    strForm += w
                M.loc[A][b].append(curPro)
                outM.loc[A][b] += "    " + strForm


getM()
strM = str(outM)


# tb=Texttable()
# # tb.set_cols_align(['l','r','r'])
# # tb.set_cols_dtype(['t','i','i'])
# tb.header(outM.columns)
#
# tb.add_rows(outM.values,header=False)
# tb.set_max_width(300)
'''
header=False表示不将第一参数的第一行作为标题,
这样我们之前的添加的标题就会起作用了
'''
print(outM)
print(M)
f3.write("预测分析表：\n")
f3.write(str(outM))


#
# f3.write("预测分析表:\n")
# f3.write(strM)
f3.close()


# 构造LL型分析函数
def getRes(lang):
    global f
    V = lang.split(' ')
    V.append('#')
    l = len(V)
    i = 0
    # 生成初始栈
    sta = Stack()
    sta.push('#')
    sta.push('E')

    X = sta.top()
    # print('输入', ''.join(V))
    while X != '#':
        a = V[i]
        print("X:"+X)
        print("a:"+a)
        if X == a:
            sta.pop()
            i = i + 1
            print('匹配', a)
            # V = V.pop(i)
        elif X in vt:
            # raise Exception('Errof:the first sign is vt', X)
            print("错误，产生式左部是终结符")
            i = i + 1
            f = 1
            continue
        elif not M[a][X]:
            # raise Exception('Errof:not found in analysis list', X)
            print("错误，并未找到对应的文法")
            i = i + 1
            f = 1
            continue
        elif M[a][X][0] in productions:
            prod = M[a][X][0]
            # print('输出', prod[0]+" -> ")

            # 打印输出的文法
            print("Input：：", ''.join(V[i:]))
            print("OutPut ：", end='')
            print(prod[0], end=' -> ')
            for rPord in prod[1:]:
                print(rPord, end=" ")
            print()
            sta.pop()
            ll = len(prod)
            for ii in range(ll - 1):
                if prod[ll - ii - 1] != 'epsilon':
                    sta.push(prod[ll - ii - 1])
        X = sta.top()
        print('Stack :', sta.show())
        print()

    if f == 1:
        print("上文有错误")
    elif sta.top() == '#':
        print("正确")


sentence = "i + ( i * + i )"
getRes(sentence)



