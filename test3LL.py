from test1Cifa import filterResource, Scan

MAX = 100

c = ['i', '(', '+', '-', '*', '/', ')', '#']
w = ['E', 'e', 'T', 't', 'F', 'A', 'M']
mapp = [["Te", "Te", "%", "%", "%", "%", "%", "%"],
        ["%", "%", "ATe", "ATe", "%", "%", "#", "#"],
        ["Ft", "Ft", "%", "%", "%", "%", "%", "%"],
        ["%", "%", "#", "#", "MFt", "MFt", "#", "#"],
        ["i", "(E)", "%", "%", "%", "%", "%", "%"],
        ["%", "%", "+", "-", "%", "%", "%", "%"],
        ["%", "%", "%", "%", "*", "/", "%", "%"]]


class Stack(object):

    def __init__(self):
        # 创建空列表实现栈
        self.__list = []

    def empty(self):
        # 判断是否为空
        return self.__list == []

    def push(self, item):
        # 压栈，添加元素
        self.__list.append(item)

    def pop(self):
        # 弹栈，弹出最后压入栈的元素
        if self.empty():
            return
        else:
            return self.__list.pop()

    def top(self):
        # 取最后压入栈的元素
        if self.empty():
            return
        else:
            return self.__list[-1]


def panduan(ch):
    for i in range(8):
        if ch == c[i]:
            return True
    return False


def findc(ch):
    # print(list(ch.keys())[0])
    if ch.isdigit():
        return 0
    for i in range(8):
        if ch == c[i]:
            return i

    return 0


def findw(ch):
    for i in range(7):
        if ch == w[i]:
            return i
    return 0


if __name__ == '__main__':


    filterResource("out.txt", "test.txt")
    tok = Scan("out.txt")


    strli = ''.join(open("test3.txt", 'r').readlines())

    # 提取出来的tok是一个个元组的列表
    strli = tok

    # 把元组的列表合并
    stritem = dict()
    for li in strli:
        stritem.update(li)

    # 把元组的key单独提出来放到一个列表
    str = list(stritem.keys())
    str.remove(";")
    print("str :")
    print(str)
    q = Stack()
    ip = 0
    q.push('#')
    q.push('E')

    while not q.empty():

        ch = q.top()
        if ch == '#':
            break
        i = findw(ch)
        # print("ip:")
        # print(ip)
        j = findc(str[ip])
        if ch == str[ip]:

            q.pop()
            print("匹配" + str[ip])
            # cout << "匹配" << str[ip] << endl;
            ip = ip + 1
        elif str[ip] and ch == 'i':
            q.pop()
            print(ch + "->" + str[ip])
            print("匹配" + str[ip])
            # cout << ch << "->" << str[ip] << endl;
            # cout << "匹配" << str[ip] << endl;
            ip = ip + 1

        elif panduan(ch):

            print("不匹配")
            exit(0)

        elif mapp[i][j][0] == '%':

            print("不比配")
            exit(0)

        elif mapp[i][j][0] == '#':
            print(ch + "->" + "#")
            # cout << ch << "->" << "#" << endl;
            q.pop()

        else:

            n = len(mapp[i][j])
            q.pop()
            for k in range(n - 1, -1, -1):
                # (int k=n-1;k >= 0;k--)

                q.push(mapp[i][j][k])
                print(ch + "->" + mapp[i][j])
                # cout << ch << "->" << mapp[i][j] << endl;

