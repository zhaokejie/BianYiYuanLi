# 去掉注释,获取文件
import re
import string


# 对代码进行预处理，去除注释以及空格
def filterResource(new_file, file):
    f2 = open(new_file, 'w+')
    txt = ''.join(open(file, 'r').readlines())
    # 用正则表达式处理注释
    data_txt = re.sub(r'\#.*', '', txt)

    # 删除空格制表符和换行符
    for line in data_txt.split('\n'):
        line = line.strip()
        line = line.replace('\\t', '')
        line = line.replace('\\n', '')

        # line = ' '.join(line.split())

        if not line:
            continue
        else:
            f2.write(line)

    # 在末尾添加#供实验二使用
    f2.write("#")
    f2.close()


def Scan(file):
    # 定义分割符运算符和关键字
    operator = ['>', '<', '=', ':=', '>=', '<=', '<>', '++', '--', '+', '-', '*', '/', ':', '+=', '-=', '*=', '/=']
    key = ['begin', 'end', 'if', 'then', 'else', 'for', 'while', 'do', 'and', 'or', ' not']
    delimiters = ['(', ')', ';', '#']


    token = []
    global flage
    flage = 1
    data = open(file, 'r').readlines()


    # 实际上该层循环只进行了一次,因为读入的只有一行
    for line in data:
        flage = 1
        word = ''
        word_line = []
        i = 0

        while i < len(line):
            word += line[i]

            l = line[i]
            if (l not in operator) and (l not in key) and  (l not in delimiters) and \
                    (not(l in string.ascii_letters or l in string.digits or l == '_' or l is ' ')):

                syx = '非法字符'
                word_line.append({word: syx})
                i += 1
                word = ''
                continue

            # 判断扫描指针到达分隔符或者空格或者一个运算符,停止判断前面的单词成分
            if line[i] == ' ' or (line[i] in delimiters) or (line[i] in operator):

                # 判断非法标识符
                if word[0] in string.digits:
                    for j in word[1:]:
                        if j in string.ascii_letters or j == '_':
                            syx = '非法字符'
                            word_line.append({word: syx})
                            flage = 0
                            break
                    if flage == 0:
                        # i += 1
                        word = ''
                        continue


                # 如果首字符是下划线或者字母,考虑是不是标识符
                # print(word)
                if word[0].isalpha() or word[0] == '_':
                    word = word[:-1]

                    # 用循环判断该单词每一个非首字符的其他字符是不是字母或者数字
                    for j in word[1:]:
                        flage = 1
                        if (j in string.ascii_letters or j in string.digits or j == '_') == 1:
                            # print("succ")
                            continue
                        else:
                            print(word + '中含有非法字符')
                            flage = 0
                            break
                    if flage:
                        if word in key:
                            syx = '关键字'

                            word_line.append({word: syx})
                        else:
                            syx = '标识符ID'

                            word_line.append({word: syx})
                    else:
                        syx = '非法字符'
                        word_line.append({word: syx})
                elif word[:-1].isdigit():
                    syx = '无符号整数NUM'
                    word_line.append({word[:-1]: syx})

                if line[i] in delimiters:
                    syx = '分界符'
                    word_line.append({line[i]: syx})
                elif line[i] in operator:
                    syx = '运算符'
                    if i < len(line) - 1:
                        s = line[i] + line[i + 1]
                        if s in operator:
                            word_line.append({s: syx})
                            i += 1
                        else:
                            word_line.append({line[i]: syx})
                word = ''
            i += 1
        # 循环将词法分析判断好的键值对写入字典
        token.append(word_line)
    tok = token[0]

    # 打印词法分析后的产生的字典
    for kxx in range(0, len(tok)):
        print(kxx + 1, tok[kxx])
    return tok





if __name__ == '__main__':
    filterResource("testPreDeal.txt", "test1.txt")
    Scan("testPreDeal.txt")
