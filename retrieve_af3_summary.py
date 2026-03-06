import os
import json
import pandas as pd
from pathlib import Path
from pdb import set_trace


# 设置路径
# base_dir = Path(r"C:\Users\王成\Downloads\hbm_design_af3")
base_dir = Path(r"C:\Users\王成\Downloads\folds_2025_08_22_06_22")
csv_path = Path(r"C:\Users\王成\Downloads\all_model_0_files\rmsd_results.csv")
output_csv = csv_path.parent / "rmsd_results_with_iptm.csv"

# 读取CSV文件
df = pd.read_csv(csv_path)

# 创建存储iptm值的列表
iptm_values = []

# 遍历CSV文件的每一行
for _, row in df.iterrows():
    cif_file = row["CIF File"]
    
    # 提取子文件夹名称（去除fold_前缀和_model_0.cif后缀）
    folder_name = cif_file.replace("fold_", "").replace("_model_0.cif", "")
    
    # 构建JSON文件路径
    json_file = base_dir / folder_name / f"fold_{folder_name}_summary_confidences_0.json"
    
    # 读取JSON文件并提取chain_iptm[0]
    with open(json_file, 'r') as f:
        data = json.load(f)
        iptm = data["chain_iptm"][0]
        iptm_values.append(iptm)

# 添加iptm列到DataFrame
df["chain_iptm"] = iptm_values

# 保存结果到新CSV文件
df.to_csv(output_csv, index=False)
print(f"处理完成！结果已保存至: {output_csv}")