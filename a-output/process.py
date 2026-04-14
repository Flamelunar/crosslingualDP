def read_and_process_file(input_file, output_file):
    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 跳过第一行（total-num=68）
    lines = lines[1:]

    # 解析标签和数量
    label_counts = {}
    total_count = 0
    for line in lines:
        label, count = line.strip().split('\t')
        count = int(count)
        label_counts[label] = count
        total_count += count

    # 计算每种标签的百分比
    label_percentages = {label: (count / total_count) * 100 for label, count in label_counts.items()}

    # 将结果写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for label, count in label_counts.items():
            percentage = label_percentages[label]
            f.write(f"{label}\t{count}\t{percentage:.2f}%\n")

# 使用示例
input_file = '/home/ljj/2-biaffine-taketurn-2paper/a-output/dict-zh-ud/labels'
output_file = '/home/ljj/2-biaffine-taketurn-2paper/a-output/result/labels-zh'
read_and_process_file(input_file, output_file)