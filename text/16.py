import re
import sys

def check_line(line):
    # 查找所有在 > 和 < 之间的内容（非贪婪匹配）
    matches = re.findall(r'>([^<]+)<', line)
    # 检查是否存在长度超过16的匹配项
    return any(len(match) > 16 for match in matches)

def main():
    # 从标准输入或文件读取内容
    for line in sys.stdin:
        if check_line(line):
            print(line.strip())

if __name__ == "__main__":
    main()







import re

with open('dsoc_event.bin', 'r', encoding='utf-8') as file:
    for line in file:
        # 查找所有>和<之间的内容
        matches = re.findall(r'>([^<]+)<', line)
        # 检查是否有任何匹配项长度超过16
        if any(len(match) > 16 for match in matches):
            print(line, end='')
