import re

# 假设你的文件名为 input.txt，结果将保存在 output.txt 中
input_filename = '/home/ljj/3-biaffine-taketurn/data/ud-2.13/src/en_ewt-ud-train.conllu'  # 替换为你的输入文件路径
output_filename = '/home/ljj/3-biaffine-taketurn/data/ud-2.13/src/en_ewt-ud-train-1.conllu'  # 替换为你的输出文件路径

# 定义匹配以 "http://www" 开头的网址的正则表达式
url_pattern = re.compile(r'^http://www.*')

# 打开原始文件和输出文件
with open(input_filename, 'r', encoding='utf-8') as file, \
     open(output_filename, 'w', encoding='utf-8') as output_file:
    # 逐行读取文件
    for line in file:
        # 将行分割为列
        columns = line.strip().split('\t')
        # 创建一个新的列列表用于存储替换后的列
        new_columns = []
        for column in columns:
            # 如果列以 "http://www" 开头，则替换为 "<unk>"
            if url_pattern.match(column):
                new_columns.append('<unk>')
            else:
                new_columns.append(column)
        # 将替换后的列列表合并为一行，并写入输出文件
        output_file.write('\t'.join(new_columns) + '\n')

print("处理完成，结果保存在", output_filename)