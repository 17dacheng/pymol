from pymol import cmd, stored

def analyze_epitope(antigen_chain, fv_selection="chain H or chain L", cutoff_dist=8.0, dASA_cutoff=0.75, epitope_name="epitope"):
    """
    分析FV抗体在指定抗原链上的表位残基。
    """
    # 生成唯一的选择对象名称，避免冲突
    temp_complex = "temp_complex"
    temp_antigen = "temp_antigen"
    temp_fv = "temp_fv"
    nearby_resi_selection = "nearby_resi"
    
    # 创建复合物和工作副本
    cmd.create(temp_complex, "all")
    cmd.disable("all")
    cmd.enable(temp_complex)
    
    # 1. 基于距离进行初步筛选
    cmd.select(nearby_resi_selection, f"byres ({antigen_chain} within {cutoff_dist} of ({fv_selection}))")
    
    # 如果附近没有残基，直接返回空列表
    if cmd.count_atoms(nearby_resi_selection) == 0:
        print(f"Warning: No residues found on {antigen_chain} within {cutoff_dist} Å of FV antibody.")
        cmd.delete(temp_complex)
        cmd.delete(nearby_resi_selection)
        return []
    
    # 2. 提取抗原链和FV抗体链
    cmd.extract(temp_antigen, f"{temp_complex} and {antigen_chain}")
    cmd.extract(temp_fv, f"{temp_complex} and ({fv_selection})")
    
    # 3. 计算复合物中目标残基的SASA
    cmd.get_area(temp_complex, load_b=1)
    cmd.alter(temp_complex, "q=b")
    
    # 4. 计算抗原链单独存在时的SASA
    cmd.get_area(temp_antigen, load_b=1)
    
    # 5. 计算dASA = SASA(单独抗原链) - SASA(复合物)
    stored.residues_dASA = []
    cmd.iterate(nearby_resi_selection, "stored.residues_dASA.append((chain, resi, resn, b - q))")
    
    # 6. 根据dASA阈值筛选表位残基
    epitope_residues = []
    selection_expression = ""
    for (chain, resi, resn, dASA) in stored.residues_dASA:
        if dASA >= dASA_cutoff:
            epitope_residues.append((chain, resi, resn, dASA))
            if selection_expression:
                selection_expression += " or "
            selection_expression += f"(chain {chain} and resi {resi})"
    
    # 7. 创建表位选择对象并可视化 - 这里是修复的关键行
    if epitope_residues:
        # 修复：在[-1]后面添加了缺少的闭合方括号
        final_epitope_name = f"{epitope_name}_{antigen_chain.split()[-1]}"  # 例如 epitope_A
        cmd.select(final_epitope_name, selection_expression)
        cmd.show("sticks", final_epitope_name)
        cmd.color("red", final_epitope_name)
        print(f"表位 {final_epitope_name} 已创建，包含 {len(epitope_residues)} 个残基。")
    else:
        print(f"Warning: No epitope residues found on {antigen_chain} using dASA cutoff {dASA_cutoff}.")
    
    # 8. 清理临时对象
    cmd.delete(temp_complex)
    cmd.delete(temp_antigen)
    cmd.delete(temp_fv)
    cmd.delete(nearby_resi_selection)
    cmd.enable("all")
    
    return epitope_residues

# 将函数扩展到PyMOL命令中
cmd.extend("analyze_epitope", analyze_epitope)

print("Epitope analysis script loaded successfully. Use 'analyze_epitope antigen_chain=\"chain A\"' to analyze interactions.")