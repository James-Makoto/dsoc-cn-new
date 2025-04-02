import re

# 输入文件路径
input_file = input("请输入要处理的文件路径：")
# 输出文件名
output_file = "超字"

with open(input_file, 'r', encoding='utf-8') as f_in:
    with open(output_file, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            # 去除行尾换行符后检查长度
            if len(line.rstrip('\n')) > 20:
                # 写入原行内容（保留原有换行符）
                f_out.write(line)