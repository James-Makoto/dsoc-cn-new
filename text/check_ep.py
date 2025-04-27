import json
import re

def check_punctuation_consistency(json_file):
    """检查JSON文件中Jpn末尾有全角标点但Chs没有的条目（跳过Chs为空的情况）"""
    # 定义全角标点符号
    fullwidth_punctuation = r'[。！？…．，、]'
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)  # 读取整个JSON文件
    
    for entry in data:
        jpn = entry.get("Jpn", "")
        chs = entry.get("Chs", "")
        
        # 如果Chs为空，直接跳过
        if not chs:
            continue
        
        # 检查Jpn末尾是否有全角标点（包括<br>后的情况）
        jpn_has_punct = re.search(
            fr'{fullwidth_punctuation}\s*(<br>\s*)?$', 
            jpn
        )
        
        if jpn_has_punct:
            # 检查Chs末尾是否有全角标点
            chs_has_punct = re.search(
                fr'{fullwidth_punctuation}\s*(<br>\s*)?$', 
                chs
            )
            
            if not chs_has_punct:
                print(f"不一致发现 - No.: {entry.get('No.', '?')}, File: {entry.get('File', '?')}")
                print(f"Jpn: {jpn}")
                print(f"Chs: {chs}")
                print("-" * 50)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("请指定JSON文件路径，例如: python script.py data.json")
        sys.exit(1)
    
    json_file = sys.argv[1]
    print(f"开始检查 {json_file} 的标点符号一致性...\n")
    check_punctuation_consistency(json_file)
    print("\n检查完成。")