
import os
import re

# Terminology mapping: Mainland/General -> Taiwan Preferred
mapping = {
    "網絡": "網路",
    "分佈式": "分散式",
    "帶寬": "頻寬",
    "數據": "資料",
    "算法": "演算法",
    "存儲": "儲存",
    "內存": "記憶體",
    "優化": "最佳化",
    "哈希": "雜湊",
    "範式": "典範",
    "魯棒": "強健",
}

computing_mapping = {
    "計算能力": "運算能力",
    "計算開銷": "運算開銷",
    "計算消耗": "運算消耗",
    "計算複雜度": "運算複雜度",
    "計算資源": "運算資源",
    "計算通用性": "運算通用性",
    "計算出的": "運算出的",
    "計算結果": "運算結果",
    "重新計算": "重新運算",
    "計算聚合": "運算聚合",
}

information_mapping = {
    "信息複雜度": "訊息複雜度",
    "公開信息": "公開資訊",
    "信息": "資訊", 
}

def fix_file(filepath):
    print(f"Processing {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Apply unambiguous mappings
        for old, new in mapping.items():
            if old == "算法":
                # Special case to avoid "演演算法"
                content = content.replace("演算法", "算法") # Revert any already converted ones to base
                content = content.replace("算法", "演算法")
            else:
                content = content.replace(old, new)

        for old, new in computing_mapping.items():
            content = content.replace(old, new)

        for old, new in information_mapping.items():
            content = content.replace(old, new)

        # Handle "計算" vs "運算" carefully
        content = content.replace("運算", "計算") # Revert to base
        content = content.replace("計算", "運算")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully updated {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

target_dir = "latex-thesis/chapters"
if os.path.exists(target_dir):
    for filename in os.listdir(target_dir):
        if filename.endswith(".tex"):
            fix_file(os.path.join(target_dir, filename))
else:
    print(f"Directory {target_dir} does not exist!")

md_files = ["chapters/abstract.md", "chapters/introduction.md", "chapters/background.md", "chapters/evaluation.md", "chapters/framework-design.md", "chapters/related-work.md", "chapters/threat-model.md"]
for md_file in md_files:
    if os.path.exists(md_file):
        fix_file(md_file)
    else:
        print(f"File {md_file} does not exist!")
