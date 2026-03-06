import os
import shutil
from pdb import set_trace

# 设置源文件夹路径
data_dir = r"D:\0 公司项目\2 抗体设计\VHH Template\af3_complex"

# 创建新文件夹路径（与源文件夹同级）
parent_dir = os.path.dirname(data_dir)
target_dir = os.path.join(parent_dir, "all_model_0_files")

# 确保目标文件夹存在
if not os.path.exists(target_dir):
    os.makedirs(target_dir)
    print(f"创建目标文件夹: {target_dir}")

# 遍历所有子文件夹
for subdir_name in os.listdir(data_dir):
    subdir_path = os.path.join(data_dir, subdir_name)
    
    # 确保是文件夹而非文件
    if os.path.isdir(subdir_path):
        file_found = False
        files = os.listdir(subdir_path)
        
        # 递归搜索目标文件
        for file in files:
            if "_model_0.cif" in file:
                src_file = os.path.join(subdir_path, file)
                dst_file = os.path.join(target_dir, file)
                
                # 复制文件
                shutil.copy2(src_file, dst_file)
                print(f"已复制: {os.path.basename(src_file)} -> {dst_file}")
                file_found = True
                break  # 找到文件后跳出当前子文件夹遍历
        
        if not file_found:
            print(f"未找到: {subdir_name} 中缺少 _model_0.cif 文件")

print(f"\n操作完成! 共处理 {len(os.listdir(data_dir))} 个子文件夹")