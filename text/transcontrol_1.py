import re

def process_text(input_file):
    # 读取文件内容
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 替换
    content = content.replace('<br>', '')
    content = content.replace('<p>', '\n')
    content = content.replace('<cn=000C>', '【姓】')
    content = content.replace('<cn=0000>', '【名】')
    content = content.replace('<cn=000D>', '【主角昵称】')
    content = content.replace('▷', '！？')
    content = content.replace('▶', '！！')
    # 删除所有<...>内的内容
    content = re.sub(r'<vd=.*?>', '', content)
    content = re.sub(r'<vp=.*?>', '', content)
    content = re.sub(r'<vbd=.*?>', '', content)
    content = re.sub(r'<vdd=.*?>', '', content)
    content = re.sub(r'<c=.*?>', '', content)

    # 保存处理后的内容
    with open('原文.txt', 'w', encoding='utf-8') as file:
        file.write(content)

# 使用示例
input_file = input("请输入要处理的文件路径：")
process_text(input_file)
print("处理完成，结果已保存为 原文.txt")
