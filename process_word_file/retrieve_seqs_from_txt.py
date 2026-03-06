import os
import re
import sys
from pdb import set_trace

def extract_sequences(content, filename):
    """
    分块提取pTH序列：先按pTH*或关键词分割，再在各块中定位序列
    1. 分块时保留分隔符（pTH*或"氨基酸序列"）
    2. 在块内根据上下文定位实际序列
    """
    sequences = []
    
    # 步骤1：同时捕获pTH标识符和"氨基酸序列"作为分隔符
    blocks = re.split(r'(pTH\d+)', content, flags=re.IGNORECASE)
    if len(blocks) < 3:
        return sequences
    
    # 步骤2：遍历块并关联标识符与序列
    sequences = []
    current_id = None
    aa_chars = "ACDEFGHIKLMNPQRSTVWYBZX"  # 氨基酸字符集

    for i, block in enumerate(blocks):
        # 识别pTH标识符
        if re.match(r'pTH\d+', block, re.IGNORECASE):
            current_id = block.strip()
        
        # 识别氨基酸序列关键字后的序列
        elif "氨基酸序列" in block and current_id:
            seq_match = re.search(r'氨基酸序列[^\w]*([A-Z\s]+?)(?=\s|\t|\Z)', 
                                block, re.IGNORECASE | re.DOTALL)
            
            if not seq_match:
                pattern = r'氨基酸序列[^\w]*([A-Z0-9\s-]+?)(?=\s*\轻链|\Z)'
                seq_match = re.search(pattern, block, re.IGNORECASE | re.DOTALL)

            if seq_match:
                aa_seq = seq_match.group(1)
                cleaned_seq = re.sub(r'\s+', '', aa_seq)
                sequences.append((current_id, cleaned_seq))
            
        
        # 处理antibody关键字后的序列
        elif "antibody" in block.lower() and current_id:
            seq_match = re.search(r'antibody[^\w]*([A-Z\s]+?)(?=\s|\t|\Z)', 
                                block, re.IGNORECASE | re.DOTALL)
            if seq_match:
                aa_seq = seq_match.group(1)
                cleaned_seq = re.sub(r'\s+', '', aa_seq)
                sequences.append((current_id, cleaned_seq))
                
        # 新增：处理长氨基酸序列（无关键字）
        elif current_id and re.search(rf"[{aa_chars}]{{81,}}", block):
            # 找到所有可能的氨基酸序列段
            possible_seqs = re.findall(rf"[{aa_chars}]+", block)
            if possible_seqs:
                # 选择最长的连续序列
                long_seq = max(possible_seqs, key=len)
                if len(long_seq) >= 80:
                    sequences.append((current_id, long_seq))
    
    # if filename == 'word.to.txt.janqi.com__THP00011-THP00014.txt':
    #     set_trace()
    return sequences

def format_fasta(sequences):
    """将序列格式化为FASTA格式（每60个氨基酸换行）"""
    fasta_content = []
    for seq_id, seq in sequences:
        # 检查并去除特定前缀
        if seq.startswith("MHSSALLCCLVLLTGVRA"):
            seq = seq[len("MHSSALLCCLVLLTGVRA"):]
        if seq.startswith("MGWSCIILFLVATATGVHS"):
            seq = seq[len("MGWSCIILFLVATATGVHS"):]
        
        fasta_content.append(f">{seq_id}")
        for i in range(0, len(seq), 60):
            fasta_content.append(seq[i:i+60])
    return "\n".join(fasta_content)

def process_files(input_folder, output_folder):
    """处理文件夹中所有txt文件，生成FASTA文件"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    processed_files = 0
    for filename in os.listdir(input_folder):
        if not filename.endswith('.txt'):
            continue
            
        input_path = os.path.join(input_folder, filename)
        
        # 去除文件名中的特定前缀
        clean_filename = re.sub(r'word\.to\.txt\.janqi\.com__', '', filename)
        output_path = os.path.join(output_folder, clean_filename.replace('.txt', '.fasta'))
        
        try:
            with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            sequences = extract_sequences(content, filename)
            
            if sequences:
                with open(output_path, 'w') as out_file:
                    out_file.write(format_fasta(sequences))
                print(f"已生成: {output_path} ({len(sequences)}条序列)")
                processed_files += 1
            else:
                print(f"警告: {filename} 未找到有效序列")
        except Exception as e:
            print(f"处理文件 {filename} 时出错: {str(e)}")
    
    return processed_files

if __name__ == "__main__":
    input_folder = r'C:\Users\王成\Downloads\天衡蛋白库\word.to.txt.janqi.com'
    output_folder = os.path.join(input_folder, 'fasta_output')
    
    print(f"开始处理文件夹: {input_folder}")
    processed_count = process_files(input_folder, output_folder)
    print(f"\n处理完成! 共处理 {processed_count} 个文件")
    print(f"FASTA文件保存在: {output_folder}")