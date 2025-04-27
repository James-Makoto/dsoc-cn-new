import re
import json
import sys

def check_halfwidth_in_file(json_file):
    """
    检测非法半角字符（完整排除 %s、&d 等占位符）
    """
    issues = []
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"文件读取失败: {e}")
        return []

    # 需要保留的完整占位符模式（不会被检测）
    PLACEHOLDERS = [
        r'%s',    # 字符串占位符
        r'%d',    # 数字占位符
        r'&s',    # 特殊指令
        r'&d',    # 特殊指令
        r'<[^>]+>' # 所有标签
    ]
    
    for entry in data:
        if "Chs" not in entry or not entry["Chs"]:
            continue
            
        chs_text = entry["Chs"]
        
        # 方法1：先移除占位符再检测
        clean_text = chs_text
        for ph in PLACEHOLDERS:
            clean_text = re.sub(ph, '', clean_text)
        
        # 方法2（更精确）：标记占位符位置后检测
        placeholder_pos = set()
        for ph in PLACEHOLDERS:
            for m in re.finditer(ph, chs_text):
                placeholder_pos.update(range(m.start(), m.end()))
        
        illegal_chars = []
        char_positions = []
        for i, char in enumerate(chs_text):
            # 只检测非占位符部分的半角字符
            if i not in placeholder_pos and ord(char) in range(0x20, 0x7F):
                illegal_chars.append(char)
                char_positions.append(i)
        
        if illegal_chars:
            issues.append({
                "No.": entry.get("No.", "N/A"),
                "File": entry.get("File", "N/A"),
                "原始文本": chs_text,
                "非法字符": illegal_chars,
                "字符位置": char_positions,
                "诊断": f"发现 {len(illegal_chars)} 处非占位符半角字符"
            })
    
    return issues

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python script.py your_file.json")
        sys.exit(1)

    problems = check_halfwidth_in_file(sys.argv[1])
    
    if problems:
        print(f"发现 {len(problems)} 处问题（已排除占位符）:")
        for idx, prob in enumerate(problems, 1):
            print(f"\n#{idx} [No.{prob['No.']}]")
            print(f"文件: {prob['File']}")
            print(f"原文: {prob['原始文本']}")
            print(f"非法字符: {prob['非法字符']} (位置: {prob['字符位置']})")
            print(f"诊断: {prob['诊断']}")
    else:
        print("检测完成，未发现非法半角字符")