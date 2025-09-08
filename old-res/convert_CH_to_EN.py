import json
import os

# 定义中英文键名映射
key_mapping = {
    # 主键映射
    "签号": "id",
    "签题": "title",
    "吉凶": "luck",
    "签诗": "poem",
    "总判": "summary",
    "解析": "analysis",
    
    # 解析子项映射
    "功名": "career",
    "婚姻": "marriage",
    "求财": "wealth",
    "疾病": "health",
    "诉讼": "lawsuit",
    "行人": "traveler",
    "年成": "harvest",
    "求嗣": "offspring",
    "移居": "relocation",
    "失物": "lost_property",
    "出行": "travel",
    "家宅": "household",
    "六甲": "pregnancy",
    "谋望": "plans",
    "自身": "personal"
}

# 吉凶类型映射
luck_mapping = {
    "上上签（大吉）": "supreme_luck",
    "上上签": "supreme_luck",
    "上吉签": "great_luck",
    "上中签": "good_luck",
    "中吉签": "medium_luck",
    "中平签": "neutral_luck",
    "下下签": "bad_luck"
}

def convert_luohanqian(input_file, output_file):
    # 读取原始JSON文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    converted_data = {}
    
    # 处理每一签
    for sign_key, sign_data in data.items():
        converted_sign = {}
        
        # 转换主键
        for cn_key, en_key in key_mapping.items():
            if cn_key in sign_data:
                # 特殊处理吉凶字段
                if cn_key == "吉凶":
                    luck_value = sign_data[cn_key]
                    converted_sign[en_key] = luck_mapping.get(luck_value, luck_value)
                else:
                    converted_sign[en_key] = sign_data[cn_key]
        
        # 转换解析子项
        if "analysis" in converted_sign:
            converted_analysis = {}
            for cn_key, value in sign_data["解析"].items():
                en_key = key_mapping.get(cn_key, cn_key)
                converted_analysis[en_key] = value
            converted_sign["analysis"] = converted_analysis
        
        # 使用新键名存储
        new_sign_key = sign_key.replace("第", "sign_").replace("签", "")
        converted_data[new_sign_key] = converted_sign
    
    # 写入转换后的JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(converted_data, f, ensure_ascii=False, indent=2)
    
    print(f"转换完成！输出文件已保存至: {output_file}")

# 使用示例
if __name__ == "__main__":
    input_file = "luohanqian.json"  # 原始文件路径
    output_file = "luohanqian_en.json"  # 转换后文件路径
    
    # 检查文件是否存在
    if not os.path.exists(input_file):
        print(f"错误：输入文件 {input_file} 不存在")
    else:
        convert_luohanqian(input_file, output_file)