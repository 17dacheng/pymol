from Bio.PDB import MMCIFParser, PDBIO
import os

def convert_cif_to_pdb(cif_file_path, output_dir="."):
    """
    将 mmCIF 文件转换为 PDB 格式
    :param cif_file_path: 输入的 CIF 文件路径
    :param output_dir: 输出目录（默认为当前目录）
    :return: 生成的 PDB 文件路径
    """
    try:
        # 验证输入文件
        if not os.path.exists(cif_file_path):
            raise FileNotFoundError(f"CIF 文件不存在: {cif_file_path}")
        if not cif_file_path.lower().endswith(('.cif', '.mmcif')):
            print(f"警告: 文件扩展名非标准 CIF 格式: {cif_file_path}")

        # 从文件名提取结构标识符（不含扩展名）
        structure_id = os.path.basename(cif_file_path).split('.')[0]
        
        # 创建解析器和结构对象
        parser = MMCIFParser(QUIET=True)  # 禁用解析警告
        structure = parser.get_structure(structure_id, cif_file_path)
        
        # 准备输出路径
        os.makedirs(output_dir, exist_ok=True)
        pdb_file_path = os.path.join(output_dir, f"{structure_id}.pdb")
        
        # 使用 PDBIO 写入 PDB 格式
        io = PDBIO()
        io.set_structure(structure)
        io.save(pdb_file_path)
        
        print(f"转换成功: {cif_file_path} -> {pdb_file_path}")
        return pdb_file_path

    except Exception as e:
        print(f"转换失败: {str(e)}")
        return None

# 使用示例
if __name__ == "__main__":
    input_cif = "fold_il2v_wt_bcloop_il2r_model_0.cif"  # 替换为你的CIF文件路径
    output_directory = "converted_pdbs"  # 自定义输出目录
    
    result = convert_cif_to_pdb(input_cif, output_directory)
    if result:
        print(f"PDB 文件已保存至: {result}")