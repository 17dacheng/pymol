from Bio import SeqIO
from Bio.Align import PairwiseAligner, substitution_matrices

# 读取两个FASTA文件中的第一条序列
seq1 = next(SeqIO.parse("human.fasta", "fasta")).seq
seq2 = next(SeqIO.parse("mouse.fasta", "fasta")).seq

# 配置比对器（使用蛋白质矩阵）
aligner = PairwiseAligner()
aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")  # 加载BLOSUM62矩阵
aligner.open_gap_score = -10  # 空位开启罚分
aligner.extend_gap_score = -0.5  # 空位延伸罚分

# 执行全局比对并取最优结果
alignments = aligner.align(seq1, seq2)
best_alignment = alignments[0]

# 获取相同残基数量（关键修正点！）
matches = best_alignment.counts().identities  # ✅ 正确属性名

# 计算相似度（按较短序列长度归一化）
similarity = matches / min(len(seq1), len(seq2)) * 100
print(f"序列相似度: {similarity:.2f}%")