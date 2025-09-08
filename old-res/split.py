import json
import math

# 加载原始数据
with open('signs.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 分割配置
TOTAL_SIGNS = 500
SIGNS_PER_FILE = 50
sign_keys = sorted(data.keys(), key=lambda x: int(x.split('_')[1]))

# 执行分割
for i in range(0, math.ceil(TOTAL_SIGNS/SIGNS_PER_FILE)):
    start = i * SIGNS_PER_FILE
    end = start + SIGNS_PER_FILE
    part = {k: data[k] for k in sign_keys[start:end]}
    
    with open(f'signs_{i+1}.json', 'w', encoding='utf-8') as f:
        json.dump(part, f, ensure_ascii=False, indent=2)

print(f'成功分割为{math.ceil(TOTAL_SIGNS/SIGNS_PER_FILE)}个文件')