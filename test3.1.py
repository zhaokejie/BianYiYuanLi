import copy

strs = ['#', 'E']  # 当做栈来使用，栈是先进后出那我就从-1开始
list1 = [['E->TE\'', '', '', '', '', 'E->TE\'', '', ''],
         ['', 'E\'->ATE\'', 'E\'->ATE\'', '', '', '', 'E\'->ε', 'E\'->ε'],
         ['T->FT\'', '', '', '', '', 'T->FT\'', '', ''],
         ['', 'T\'->ε', 'T\'->ε', 'T\'->MFT\'', 'T\'->MFT\'', '', 'T\'->ε', 'T\'->ε'],
         ['F->i', '', '', '', '', 'F->(E)', '', ''],
         ['', 'A->+', 'A->-', '', '', '', '', ''],
         ['', '', '', 'M->*', 'M->/', '', '', '']
         ]
list2 = ['E', 'E\'', 'T', 'T\'', 'F', 'A', 'M']
list3 = ['i', '+', '-', '*', '/', '(', ')', '#']
s1 = ''  # 全局变量s1


def out1():
    print("分析栈\t\t余留输入串\t\t分析表中产生式")


def out2(str1, str2, str3, str4):
    print("%s\t\t%s\t\t%s %s" % (str1, str2, str3, str4))


str1 = []
str2 = []
str3 = ''
str4 = ''
s1 = input("请输入要分析的字符串：")
s1 += '#'
for i in s1:
    str2.append(i)
out1()

for i in s1:

    while True:
        str1 = copy.copy(strs)

        sout = strs.pop()  # 取出最后一个元素

        str3 = 'M[' + sout + ',' + i + ']'
        try:

            num1 = list2.index(sout)
            num2 = list3.index(i)
            if list1[num1][num2] != '':
                schan = list1[num1][num2]
                if schan[-1] == 'ε':
                    # strs.pop()
                    strs.append(sout)
                    str1 = copy.copy(strs)
                    num1 = list2.index(strs[-1])
                    num2 = list3.index(i)
                    schan = list1[num1][num2]
                    str4 = schan
                    stop1 = 1
                    sums = ''
                    for j in schan[::-1]:
                        if j == '>':
                            break
                        elif j == '\'':
                            sums += j
                            stop1 = 2
                        else:
                            if stop1 == 1:
                                strs.append(j)
                            else:
                                sums = j + '\''
                                strs.append(sums)
                                sums = ''
                                stop1 = 1
                else:
                    str4 = schan
                    stop1 = 1
                    sums = ''
                    for j in schan[::-1]:
                        if j == '>':
                            break
                        elif j == '\'':
                            sums += j
                            stop1 = 2
                        else:
                            if stop1 == 1:
                                strs.append(j)
                            else:
                                sums = j + '\''

                                strs.append(sums)
                                sums = ''
                                stop1 = 1
        except:
            if False:
                str3 = ''
                str4 = '成功'
                out2(str1, str2, str3, str4)
                break
            else:
                str3 = 'Pop'
                str4 = 'Nextsym'
                strs.pop()
                if str1[-1] != 'ε':
                    out2(str1, str2, str3, str4)
                    str1.pop()
                    strs = copy.copy(str1)

                    break
                else:
                    str1.pop()
                    str1.pop()
                    strs = copy.copy(str1)
        if str2[-1] == '#':
            if str1[-1] == '#':
                str3 = ''
                str4 = '成功'
                out2(str1, str2, str3, str4)
                break
            elif str1[-1] != '#':
                str3 = ''
                str4 = '失败'
                out2(str1, str2, str3, str4)
                break
            else:
                str3 = ''
                if str4 != 'Nextsym':
                    out2(str1, str2, str3, str4)
        else:
            out2(str1, str2, str3, str4)

    str2.pop(0)  # 移除第一个元素