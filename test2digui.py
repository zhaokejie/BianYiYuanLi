from test1Cifa import Scan, filterResource

a = []
p = 0


def E():
    print("E->TE'\n")
    T()
    E1()


def E1():
    if a[p] == '+' or a[p] == '-':
        print("E1->ATE'\n")
        A()
        T()
        E1()
    else:
        print("E'->ε\n")


def T():
    print("T->FT'\n")
    F()
    T1()


def T1():
    if a[p] == '*' or a[p] == '/':
        print("T1->MFT'\n")
        M()
        F()
        T1()
    else:
        print("T'->ε\n")


def F():
    global p
    if a[p] == 'i':  #abc  abc
        print("F->i\n")
        p = p + 1
    else:
        if a[p] == '(':
            p = p + 1
            E()
            if a[p] == ')':
                print("F->(E)\n")
                p = p + 1

            else:
                print("error!\n")
                exit(0)
        else:
            print("error!\n")
            exit(0)


def A():
    global p
    if a[p] == '+':
        print("A->+\n")
        p = p + 1

    else:
        if a[p] == '-':
            print("A->-\n")
            p = p + 1

        else:
            print("error!\n")
            exit(0)


def M():
    global p
    if a[p] == '*':
        print("M->*\n")
        p = p + 1

    else:
        if a[p] == '/':
            print("M->/ \n")
            p = p + 1
        else:
            print("error!\n")
            exit(0)


if __name__ == '__main__':

    filterResource("testPreDeal.txt", "test1.txt")
    tok = Scan("testPreDeal.txt")
    data = ''.join(open("testPreDeal.txt", 'r').readlines())
    # print(type)
    listWord = []
    for aTok in tok:
        for a in aTok:
            # print(a)
            if '标识符ID' in aTok[a]:
                listWord.append(a)
                # data = data.replace(a, "i")
    # 对标识符进行排序，让长度长的排到前面
    listWord = sorted(listWord,key=lambda i:len(i),reverse=True)
    print("标识符列表：")
    print(listWord)
    # 对标识符进行替换，替换为i
    for word in listWord:
        data = data.replace(word, "i")
    # out2为替换标识符后的算术表达式
    f2 = open("out2.txt", 'w+')
    f2.write(data)
    a = data

    E()

    print("a[p]:"+ a[p])
    if a[p] == '#' or a[p] == ';':
        print("符合，正确")
    else:
        print("错误，不符合")

    str = "123"
