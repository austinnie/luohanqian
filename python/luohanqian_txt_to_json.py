import json
import re
from collections import OrderedDict

def clean_text(text):
    """清理文本中的特殊字符和多余空格"""
    # 移除各种不可见字符和特殊符号，包括零宽空格
    text = re.sub(r'[\u200b-\u200f\u00a0\u1680\u180e\u2028\u2029\u202f\u205f\u3000]', ' ', text)
    text = re.sub(r'[]', '', text)  # 移除零宽空格
    text = re.sub(r'\s+', ' ', text).strip()  # 合并多个空格为一个
    return text

def parse_luohanqian_text(text_content):
    """解析您提供的格式的罗汉签文本内容，更加鲁棒"""
    signs = OrderedDict()
    current_sign = None
    
    lines = text_content.split('\n')
    
    for line in lines:
        original_line = line
        line = line.strip()
        if not line:
            continue  # 跳过空行
        
        # 匹配签号，如 "第15签"，允许前后有空格
        sign_match = re.match(r'^\s*第(\d+)签\s*$', line)
        if sign_match:
            sign_num = sign_match.group(1)
            current_sign = {
                "签号": f"第{sign_num}签",
                "签题": "",
                "吉凶": "",
                "签诗": "",
                "总判": "",
                "解析": OrderedDict()
            }
            signs[f"第{sign_num}签"] = current_sign
            continue
        
        if not current_sign:
            continue  # 如果没有当前签文，跳过该行
        
        # 匹配吉凶：允许前后有空格，冒号可以是中文或英文
        luck_match = re.match(r'^\s*吉凶\s*[:：]\s*(.+?)\s*$', line)
        if luck_match:
            current_sign["吉凶"] = luck_match.group(1).strip()
            continue
        
        # 匹配签诗：允许前后有空格，冒号可以是中文或英文
        poem_match = re.match(r'^\s*签诗\s*[:：]\s*(.+?)\s*$', line)
        if poem_match:
            current_sign["签诗"] = poem_match.group(1).strip()
            continue
        
        # 匹配总判：允许前后有空格，冒号可以是中文或英文
        total_match = re.match(r'^\s*总判\s*[:：]\s*(.+?)\s*$', line)
        if total_match:
            current_sign["总判"] = total_match.group(1).strip()
            continue
        
        # 匹配各类解析：功名、婚姻、求财等
        category_match = re.match(r'^\s*(功名|婚姻|求财|疾病|诉讼|行人|年成|求嗣|移居|失物|出行|家宅|六甲|谋望|自身)\s*[:：]\s*(.+?)\s*$', line)
        if category_match:
            category = category_match.group(1)
            content = category_match.group(2).strip()
            current_sign["解析"][category] = content
            continue
    
    return signs

def convert_txt_to_json(input_file, output_file):
    """将txt文件转换为json文件"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text_content = f.read()
        
        print(f"原始文本长度: {len(text_content)}")
        # 打印前300个字符用于调试
        preview = text_content[:300].replace('\n', '\\n')
        if len(text_content) > 300:
            preview += '...'
        print(f"文本预览(前300字符): {preview}")
        
        signs_data = parse_luohanqian_text(text_content)
        
        print(f"解析到的签文数量: {len(signs_data)}")
        if signs_data:
            first_key = next(iter(signs_data))
            print(f"第一个签文示例 - 签号: {first_key}, 吉凶: {signs_data[first_key]['吉凶']}, 签诗: {signs_data[first_key]['签诗'][:30]}...")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(signs_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n转换完成！共转换 {len(signs_data)} 支罗汉签")
        print(f"数据已保存到: {output_file}")
        
        # 保存预览文件
        preview_file = "luohanqian_preview.json"
        preview_data = {}
        for i, (key, value) in enumerate(signs_data.items()):
            if i >= 15:  # 只预览前15个
                break
            preview_data[key] = {
                "签号": value["签号"],
                "吉凶": value["吉凶"],
                "签诗": value["签诗"][:50] + "..." if len(value["签诗"]) > 50 else value["签诗"],
                "总判": value["总判"][:50] + "..." if value["总判"] else "",
                "解析示例": list(value["解析"].items())[:3] if value["解析"] else []
            }
        
        with open(preview_file, 'w', encoding='utf-8') as f:
            json.dump(preview_data, f, ensure_ascii=False, indent=2)
        print(f"签文预览已保存到: {preview_file} (前15个签文)")
        
    except Exception as e:
        print(f"转换过程中发生错误：{e}")

if __name__ == "__main__":
    input_txt = "luohanqian.txt"  # 您的原始文本文件
    output_json = "luohanqian.json"  # 输出的JSON文件
    
    print(f"正在将 {input_txt} 转换为 {output_json}...")
    convert_txt_to_json(input_txt, output_json)