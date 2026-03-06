import re
import pandas as pd

def parse_mutation(mutation_str):
    """解析单个突变字符串（格式：'原始氨基酸位置突变后氨基酸'）"""
    match = re.match(r"^([A-Z])(\d+)([A-Z])$", mutation_str.strip())
    if not match:
        raise ValueError(f"无效的突变格式: '{mutation_str}'")
    
    orig_aa = match.group(1)
    position = int(match.group(2))
    mutated_aa = match.group(3)
    
    return orig_aa, position, mutated_aa

def apply_mutations(original_sequence, mutations_list):
    """应用多个氨基酸突变到序列"""
    # 验证突变位置是否重复
    positions = [mut[1] for mut in mutations_list]
    if len(positions) != len(set(positions)):
        raise ValueError("存在重复的突变位置")
    
    # 创建序列副本并应用所有突变
    mutated_sequence = original_sequence
    for orig_aa, position, mutated_aa in mutations_list:
        idx = position - 1
        if mutated_sequence[idx] != orig_aa:
            raise ValueError(f"位置{position}的氨基酸不匹配: "
                            f"预期'{orig_aa}'，实际'{mutated_sequence[idx]}'")
        mutated_sequence = mutated_sequence[:idx] + mutated_aa + mutated_sequence[idx+1:]
    
    return mutated_sequence

def main():
    # 读取输入文件
    input_file = r"C:\Users\王成\Desktop\pymol\gen_mut_txt\IL2v-T3A-C125S.txt"
    output_file = r"C:\Users\王成\Desktop\pymol\gen_mut_txt\IL2v-T3A-C125S_mutated.csv"
    
    # 解析文件内容
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    # 提取原始序列（第二行）
    original_sequence = lines[1].strip()
    
    # 处理突变记录（从第四行开始）
    results = []
    for line in lines[3:]:
        parts = line.strip().split('\t')
        if len(parts) < 3:
            continue
            
        no = parts[0]
        seq_id = parts[1]
        mutant_str = parts[2]
        
        # 解析突变字符串（可能包含多个突变）
        try:
            mutations_list = []
            for single_mut in mutant_str.split():
                # 处理复合突变（如"D84K Q11K"）
                orig_aa, position, mutated_aa = parse_mutation(single_mut)
                mutations_list.append((orig_aa, position, mutated_aa))
            
            # 应用突变到序列
            mutated_sequence = apply_mutations(original_sequence, mutations_list)
            
            results.append({
                'Seq ID.': seq_id,
                'Mutant': mutant_str,
                'Mutated Sequence': mutated_sequence
            })
        except (ValueError, IndexError) as e:
            print(f"跳过突变组合 '{mutant_str}': {str(e)}")
    
    # 创建结果DataFrame并保存
    result_df = pd.DataFrame(results)
    result_df.to_csv(output_file, index=False, sep='\t')
    
    print(f"成功生成 {len(result_df)} 个突变序列，保存至: {output_file}")

if __name__ == "__main__":
    main()