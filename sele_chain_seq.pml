# sele_chain_seq.pml
# 保存为UTF-8编码，在PyMOL命令行用"@文件路径"加载

# ===== 配置区域 =====
target_sequence = "DKTHTCPPCPAPEAAGGPSVFLFPPKPKDTLMISRTPEVTCVVVDVSHEDPEVKFNWYVDGVEVHNAKTKPREEQYNSTYRVVSVLTVLHQDWLNGKEYKCKVSNKALPAPIEKTISKAKGQPREPQVYTLPPCRDELTKNQVSLWCLVKGFYPSDIAVEWESNGQPENNYKTTPPVLDSDGSFFLYSKLTVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPGK"
chain_name = "A"  # 要搜索的链名称
output_name = "matched_seq"  # 匹配结果的对象名称

# ===== 主程序 =====
# 步骤1: 获取链A的完整序列
cmd.iterate("chain " + chain_name + " and name CA", 
            "stored.full_sequence += (oneletter if 'oneletter' in locals() else resn) + '|' + str(resi) + ' '",
            space={"stored": {"full_sequence": ""}})

# 步骤2: 提取残基编号和氨基酸序列
residue_list = []
aa_sequence = ""
for segment in stored.full_sequence.split():
    resn, resi = segment.split('|')
    residue_list.append(resi)
    aa_sequence += resn

# 步骤3: 搜索目标序列
start_idx = aa_sequence.find(target_sequence)
if start_idx == -1:
    print(f"错误: 未在链{chain_name}中找到目标序列")
else:
    # 计算匹配的残基范围
    start_res = int(residue_list[start_idx])
    end_res = int(residue_list[start_idx + len(target_sequence) - 1])
    resi_range = "+".join(residue_list[start_idx:start_idx + len(target_sequence)])
    
    # 创建选择集
    cmd.select(output_name, f"chain {chain_name} and resi {resi_range}")
    
    # 高亮显示
    cmd.show("sticks", output_name)
    cmd.color("red", output_name)
    cmd.zoom(output_name)
    
    # 打印结果
    print(f"成功匹配! 残基范围: {start_res}-{end_res}")
    print(f"创建选择对象: {output_name}")

# ===== 使用说明 ====
# 1. 将本脚本保存为UTF-8编码
# 2. 在PyMOL命令行输入: @/路径/sele_chain_seq.pml
# 3. 匹配结果将显示为红色棍状模型