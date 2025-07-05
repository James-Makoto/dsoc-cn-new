import json
import argparse
import sys
import re

def analyze_text(text):
    """分析文本并返回：
    1. 清理后的行列表（用于长度检查）
    2. 分页统计结果（每个<p>分段内的<br>数量）"""
    # 分割<p>分页
    pages = [page for page in text.split('<p>') if page.strip()]
    
    page_br_counts = []
    all_lines = []
    
    for page in pages:
        # 统计当前页的<br>数量
        br_count = page.count('<br>')
        page_br_counts.append(br_count)
        
        # 处理换行符用于长度检查
        lines = page.replace('<br>', '\n').split('\n')
        cleaned_lines = [re.sub(r'<.*?>', '', line).strip() for line in lines if line.strip()]
        all_lines.extend(cleaned_lines)
    
    return all_lines, page_br_counts

def check_text(chs_text, item_no=None, file_name=None):
    """执行两项检查：
    1. 每行是否超过19字符
    2. 每页是否超过3个<br>"""
    violations = []
    br_warnings = []
    
    lines, br_counts = analyze_text(chs_text)
    
    # 检查行长度
    for i, line in enumerate(lines, 1):
        if len(line) > 19:
            location = []
            if file_name:
                location.append(f"文件: {file_name}")
            if item_no:
                location.append(f"条目: {item_no}")
            location_str = " | ".join(location) + " | " if location else ""
            
            violations.append(
                f"{location_str}行 {i} | 长度: {len(line)} | 内容: {line}"
            )
    
    # 检查<br>数量
    for page_idx, count in enumerate(br_counts, 1):
        if count > 3:
            location = []
            if file_name:
                location.append(f"文件: {file_name}")
            if item_no:
                location.append(f"条目: {item_no}")
            location_str = " | ".join(location) + " | " if location else ""
            
            br_warnings.append(
                f"{location_str}页 {page_idx} | 包含 {count} 个<br>（超过3个）"
            )
    
    return violations, br_warnings

def main():
    parser = argparse.ArgumentParser(
        description="检查JSON文本：1)每行≤19字符 2)每页≤3个<br>"
    )
    parser.add_argument(
        "--file", "-f", 
        type=str,
        required=True,
        help="JSON文件路径（必需）"
    )
    args = parser.parse_args()

    try:
        with open(args.file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)

    all_violations = []
    all_br_warnings = []
    
    items = data if isinstance(data, list) else [data]
    for idx, item in enumerate(items, 1):
        if not isinstance(item, dict):
            continue
        
        chs_text = item.get("Chs", "")
        if not chs_text:
            continue

        violations, br_warnings = check_text(
            chs_text,
            item_no=idx,
            file_name=args.file
        )
        all_violations.extend(violations)
        all_br_warnings.extend(br_warnings)

    # 输出结果
    has_issues = False
    
    if all_br_warnings:
        has_issues = True
        print("\n以下页包含过多<br>：")
        for warning in all_br_warnings:
            print(warning)
    
    if all_violations:
        has_issues = True
        print("\n以下行超过19个字符：")
        for violation in all_violations:
            print(violation)
    
    if not has_issues:
        print("所有检查均通过：")
        print("- 没有页包含超过3个<br>")
        print("- 没有行超过19个字符")

    sys.exit(1 if has_issues else 0)

if __name__ == "__main__":
    main()