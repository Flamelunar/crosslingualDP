import re

def remove_comments(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as fr, \
         open(output_file, "w", encoding="utf-8") as fw:
        for line in fr:
            line = line.strip()
            lines = line.split("\t")  # 取出换行符

            if re.match('^#', lines[0]):
                continue

            fw.write(line)
            fw.write("\n")

# 调用函数并传入输入和输出文件路径


remove_comments("/home/ljj/3-biaffine-taketurn/data/newud/zh_gsdsimp-ud-train.conllu", "/home/ljj/3-biaffine-taketurn/data/zh_gsdsimp-ud-train.conllu")

# remove_comments("./zh-ud-train.conllu", "../data/zh-ud-train.conllu")





