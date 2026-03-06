import os
import csv
import warnings
import numpy as np
from Bio.PDB import MMCIFParser, Superimposer, Selection
from Bio.PDB.PDBExceptions import PDBConstructionWarning

# 忽略CIF解析警告
warnings.filterwarnings("ignore", category=PDBConstructionWarning)

def get_ca_atoms(chain):
    """提取链的Cα原子列表和残基ID列表"""
    ca_atoms = []
    res_ids = []
    for residue in chain:
        if residue.has_id("CA"):
            ca_atoms.append(residue["CA"])
            # 处理残基ID（考虑插入码）
            res_id = (residue.id[1], residue.id[2].strip())
            res_ids.append(res_id)
    return ca_atoms, res_ids

def find_nearest_ca(ref_atom, target_chain):
    """在目标链中查找最近的Cα原子"""
    min_distance = float("inf")
    nearest_atom = None
    
    for residue in target_chain:
        if residue.has_id("CA"):
            ca = residue["CA"]
            distance = np.linalg.norm(ref_atom.coord - ca.coord)
            if distance < min_distance:
                min_distance = distance
                nearest_atom = ca
    return nearest_atom

def calculate_rmsd(ref_chain, target_chain):
    """计算两个链之间的RMSD值"""
    ref_cas, ref_ids = get_ca_atoms(ref_chain)
    target_cas, target_ids = get_ca_atoms(target_chain)
    
    # 检查是否有足够的Cα原子
    if len(ref_cas) < 3 or len(target_cas) < 3:
        return None
    
    # 获取共同残基ID集合
    common_ids = set(ref_ids) & set(target_ids)
    
    if len(common_ids) > 3:
        # 使用共同残基进行对齐
        common_ref = [atom for atom, id in zip(ref_cas, ref_ids) if id in common_ids]
        common_target = [atom for atom, id in zip(target_cas, target_ids) if id in common_ids]
        
        sup = Superimposer()
        sup.set_atoms(common_ref, common_target)
        return sup.rms
    else:
        # 当共同残基不足时，使用最近邻方法
        aligned_ref = []
        aligned_target = []
        
        for atom in ref_cas:
            nearest = find_nearest_ca(atom, target_chain)
            if nearest:
                aligned_ref.append(atom)
                aligned_target.append(nearest)
        
        if len(aligned_ref) < 3:
            return None
        
        sup = Superimposer()
        sup.set_atoms(aligned_ref, aligned_target)
        return sup.rms

# 设置路径和参考文件
directory = r"C:\Users\王成\Downloads\all_model_0_files"
reference_file = "fold_af3_complex_1_model_0.cif"  # 改为CIF格式
reference_path = os.path.join(directory, reference_file)

# 解析参考结构 - 使用MMCIFParser
parser = MMCIFParser(QUIET=True)
ref_structure = parser.get_structure("reference", reference_path)
ref_model = next(ref_structure.get_models())
ref_chain = ref_model["A"]

# 准备结果存储
results = []
file_count = 0

# 遍历目录中的所有CIF文件
for filename in os.listdir(directory):
    if filename.endswith(".cif") and filename != reference_file:
        filepath = os.path.join(directory, filename)
        
        try:
            # 解析目标结构
            target_structure = parser.get_structure("target", filepath)
            target_model = next(target_structure.get_models())
            
            # 检查是否存在A链
            if "A" not in target_model:
                print(f"跳过 {filename}: 没有A链")
                continue
                
            target_chain = target_model["A"]
            
            # 计算RMSD
            rmsd = calculate_rmsd(ref_chain, target_chain)
            
            if rmsd is not None:
                results.append((filename, rmsd))
                file_count += 1
                print(f"已处理 {filename}: RMSD = {rmsd:.4f} Å")
            else:
                print(f"跳过 {filename}: 没有足够的Cα原子")
                
        except Exception as e:
            print(f"处理 {filename} 时出错: {str(e)}")

# 写入CSV文件
output_path = os.path.join(directory, "rmsd_results.csv")
with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["CIF File", "RMSD (Å)"])
    for filename, rmsd in results:
        writer.writerow([filename, f"{rmsd:.4f}"])

print(f"\n处理完成! 共处理 {file_count} 个文件")
print(f"结果已保存至: {output_path}")