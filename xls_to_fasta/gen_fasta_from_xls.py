import pandas as pd

# 文件路径
input_path = r'D:\vscode\pymol\xls_to_fasta\input.txt'
output_path = r'D:\vscode\pymol\xls_to_fasta\output.fasta'

# 读取制表符分隔的txt文件
df = pd.read_csv(input_path, sep='\t')

# 生成FASTA格式
with open(output_path, 'w') as f:
    for idx, row in df.iterrows():
        f.write(f'>{row["id"]}\n')
        f.write(f'{row["seq"]}\n')

print(f"FASTA文件已生成: {output_path}")
print(f"共处理了 {len(df)} 条序列")