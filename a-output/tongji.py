import pandas as pd

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Skip the first line (total-num)
    lines = lines[1:]
    
    # Parse the labels and counts
    label_counts = {}
    total_count = 0
    for line in lines:
        parts = line.strip().split('\t')
        if len(parts) == 2:
            label, count = parts
            count = int(count)
            label_counts[label] = count
            total_count += count
    
    return label_counts, total_count

def calculate_percentages(label_counts, total_count):
    return {label: (count / total_count) * 100 for label, count in label_counts.items()}

def find_common_labels(*label_dicts):
    common_labels = set.intersection(*[set(d.keys()) for d in label_dicts])
    return sorted(common_labels)

def create_table(label_percentages_list, common_labels, file_names):
    data = {'data': file_names}
    for label in common_labels:
        data[label] = [label_percentages.get(label, 0) for label_percentages in label_percentages_list]
    
    return pd.DataFrame(data)

# Read and process each file
files = {
    'golden-zh': '2-biaffine-taketurn-2paper/a-output/result/labels-zh',
    'golden-vi': '2-biaffine-taketurn-2paper/a-output/result/labels-vi',
    'ShaPri': '2-biaffine-taketurn-2paper/a-output/result/labels-shapri',
    'Our': '2-biaffine-taketurn-2paper/a-output/result/labels-our'
}

label_counts_list = []
total_counts = []
file_names = []

for name, file_path in files.items():
    label_counts, total_count = read_file(file_path)
    label_counts_list.append(label_counts)
    total_counts.append(total_count)
    file_names.append(name)

# Calculate percentages
label_percentages_list = [calculate_percentages(label_counts, total_count) for label_counts, total_count in zip(label_counts_list, total_counts)]

# Find common labels
common_labels = find_common_labels(*label_counts_list)

# Create the table
table = create_table(label_percentages_list, common_labels, file_names)

# Print the table
print(table.to_markdown(index=False))