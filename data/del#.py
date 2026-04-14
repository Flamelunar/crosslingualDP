# 假设你的文件名为 input.txt，结果将保存在 output.txt 中
import re
input_filename = '/home/ljj/3-biaffine-taketurn/UDTree/ud-treebanks-v2.13/UD_Uyghur-UDT/ug_udt-ud-test.conllu'
output_filename = '/home/ljj/3-biaffine-taketurn/data/ud-2.13/tgt/ug_ud-test.conllu'

# url_pattern = re.compile(r'^http://*')
# specific_pattern1 = '******************************************************************'
# pattern1 = re.compile(re.escape(specific_pattern1))
# pattern2 = re.compile(r'^___________*')
# pattern3 = re.compile(r'^======================*')

# 打开原始文件和输出文件
with open(input_filename, 'r', encoding='utf-8') as file, \
     open(output_filename, 'w', encoding='utf-8') as output_file:
    # 逐行读取文件
    for line in file:
        # 将行分割为列
        if not line.startswith('#') :
            columns = line.strip().split('\t')
            # if columns.
            # 检查第3列、第6列、第7列是否都是下划线
            #print(len(columns))
            if len(columns) == 1 :
                output_file.write(line) 
                          
            elif not (columns[3] == '_' or columns[6] == '_' or columns[7] == '_') :
                new_columns = []
                for column in columns:
                    # 如果列以 "http://www" 开头，则替换为 "<unk>"
                    #if url_pattern.match(column) or pattern1.match(column) or pattern2.match(column) or pattern3.match(column):
                    if len(column) > 39:
                        new_columns.append('<unk>')
                    else:
                        new_columns.append(column)
                # 将替换后的列列表合并为一行，并写入输出文件
                output_file.write('\t'.join(new_columns) + '\n')

                
print("处理完成，结果保存在", output_filename)