import openpyxl
import re
import sys

def extract_control_symbols(text):
    """提取文本中<>内的完整控制符，忽略<br>，同时检查是否有不完整的符号。"""
    # 提取完整的控制符，忽略 <br>
    symbols = set(re.findall(r'<(?!br\b)[^>]+>', text))

    # 检查不完整的控制符，检测以 < 开头但缺少右尖括号 > 的符号
    incomplete_symbols = re.findall(r'<[^>]*$', text)
    
    return symbols, incomplete_symbols

def check_control_symbols(file_path):
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active
    discrepancies = []

    # 使用 enumerate 获取行号，从第二行开始
    for row_num, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        jpn_text = row[2] or ""
        chs_text = row[3] or ""

        # 如果 CHS 列为空，则跳过检查
        if not chs_text:
            continue

        # 提取控制符和不完整的符号
        jpn_symbols, jpn_incomplete = extract_control_symbols(jpn_text)
        chs_symbols, chs_incomplete = extract_control_symbols(chs_text)

        # 检查差异
        if jpn_symbols != chs_symbols or jpn_incomplete or chs_incomplete:
            discrepancies.append({
                "row": row_num,
                "jpn_symbols": jpn_symbols,
                "chs_symbols": chs_symbols,
                "jpn_incomplete": jpn_incomplete,
                "chs_incomplete": chs_incomplete,
                "difference": jpn_symbols.symmetric_difference(chs_symbols)
            })

    # 输出结果
    if discrepancies:
        for entry in discrepancies:
            print(f"第 {entry['row']} 行:")
            print(f"  JPN控制符: {entry['jpn_symbols']}")
            print(f"  CHS控制符: {entry['chs_symbols']}")
            if entry["difference"]:
                print(f"  差异: {entry['difference']}")
            if entry["jpn_incomplete"]:
                print(f"  JPN不完整控制符: {entry['jpn_incomplete']}")
            if entry["chs_incomplete"]:
                print(f"  CHS不完整控制符: {entry['chs_incomplete']}")
    else:
        print("未发现差异或不完整控制符。")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("请提供要检查的xlsx文件路径。")
    else:
        file_path = sys.argv[1]
        check_control_symbols(file_path)
