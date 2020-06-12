# 去掉注释,获取文件
import re
import string


def filterResource(new_file, file):
    f2 = open(new_file, 'w+')
    txt = ''.join(open(file, 'r').readlines())
    data_txt = re.sub(r'\#.*', '', txt)
    for line in data_txt.split('\n'):
        line = line.strip()
        line = line.replace('\\t', '')
        line = line.replace('\\n', '')
        if not line:
            continue
        else:
            f2.write(line)
    f2.write("#")
    f2.close()


def Scan(file):
    operator = ['+', '-', '*', '/', ':', ':=', '+=', '-=', '*=', '/=']
    key = ['begin', 'end', 'if', 'then', 'else', 'for', 'while', 'do', 'and', 'or', ' not']
    delimiters = ['>', '<', '=', ':=', '>=', '<=', '<>', '++', '--', '(', ')', ';', ',', ' #']
    token = []
    global flage
    flage = 1
    # flage = 1
    data = open(file, 'r').readlines()
    for line in data:
        # print(line)
        word = ''
        word_line = []
        i = 0
        while i < len(line):
            word += line[i]
            # print(line)
            if line[i] == ' ' or (line[i] in delimiters) or (line[i] in operator):
                if word[0].isalpha() or word[0] == '_':
                    word = word[:-1]
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
        token.append(word_line)
    tok = token[0]
    for kxx in range(0, len(tok)):
        print(kxx + 1, tok[kxx])
    return tok





if __name__ == '__main__':
    filterResource("out.txt", "test.txt")
    Scan("out.txt")
