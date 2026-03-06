import itertools

def generate_mutation_combinations(input_file, output_file, max_combinations):
    """
    读取突变点文件，生成所有组合并写入输出文件。
    
    参数:
        input_file (str): 输入文件名（每行一个突变点）
        output_file (str): 输出文件名
        max_combinations (int): 最大组合数（1,2,3,...）
    """
    # 读取突变点并去除换行符
    with open(input_file, 'r') as f:
        mutations = [line.strip() for line in f if line.strip()]
    
    # 检查输入有效性
    if not mutations:
        raise ValueError("输入文件无有效突变点")
    if max_combinations < 1 or max_combinations > len(mutations):
        raise ValueError("最大组合数需在1到突变点数量之间")
    
    # 生成所有组合（从1到max_combinations）
    with open(output_file, 'w') as f_out:
        for k in range(1, max_combinations + 1):
            for combo in itertools.combinations(mutations, k):
                f_out.write(" ".join(combo) + "\n")

if __name__ == "__main__":
    input_file = "mut_xs.txt"  # 输入文件名
    output_file = input_file.replace('.txt', '_combi.txt')
    max_combinations = 3
    
    try:
        generate_mutation_combinations(input_file, output_file, max_combinations)
        print(f"生成完成！结果已保存至 {output_file}")
    except Exception as e:
        print(f"错误: {e}")