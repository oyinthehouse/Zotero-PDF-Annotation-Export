import sqlite3
import csv

# 文件路径

# SQLite 文件路径
db_path = "E:/File_Save/Zotero/zotero.sqlite" #请更换为您的SQLite文件路径
# CSV 输出文件路径
output_csv_path = "E:/File_Save/Zotero/output.csv" #请更换为您的输出CSV文件路径
# CSV输入文件路径
input_csv_path = output_csv_path
# Markdown输出文件路径
output_md_path = "E:/File_Save/Zotero/output.md" #请更换为您的输出Markdown文件路径
output_new_csv_path = "E:/File_Save/Zotero/processed_output.csv" #请更换为您的输出新CSV文件路径

# 自定义关键词，用于筛选注释
keyword = 'outputanno'

# 连接到 SQLite 数据库
conn = sqlite3.connect(db_path)
# 获取游标对象
cursor = conn.cursor()

# 步骤1: 打开 SQLite 文件，这里无需显式设置只读模式，因为我们不会执行任何写操作
# 步骤2: 查询 itemAnnotations 表，筛选 comment 包含 keyword 的记录
cursor.execute("""
SELECT parentItemID
FROM itemAnnotations
WHERE comment LIKE '%{}%'
""".format(keyword))

# 存储 parentItemID
parent_item_ids = {row[0] for row in cursor.fetchall()}

print(f"Found {len(parent_item_ids)} parentItemIDs with Keyword '{keyword}'.") # test

# 步骤3: 对每个 parentItemID，查询 itemAnnotations 表，排除包含 keyword 的记录，并写入 CSV
with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    # 写入 CSV 表头
    csv_writer.writerow(['parentItemID', 'itemID', 'type', 'text', 'comment', 'color', 'pagelabel'])

    # 遍历 parentItemID
    for parent_item_id in parent_item_ids:
        # 查询 itemAnnotations 表，包括对sortIndex的排序
        cursor.execute("""
        SELECT parentItemID, itemID, type, text, comment, color, pagelabel, sortIndex
        FROM itemAnnotations
        WHERE parentItemID = ? AND (comment NOT LIKE '%{}%' OR comment IS NULL)
        ORDER BY
        CASE WHEN sortIndex LIKE '%|%' THEN SUBSTR(sortIndex, 1, INSTR(sortIndex, '|') - 1) ELSE sortIndex END,
        CASE WHEN sortIndex LIKE '%|%' THEN SUBSTR(sortIndex, INSTR(sortIndex, '|') + 1) ELSE '0' END
        """.format(keyword), (parent_item_id,))
        
        # 获取查询结果
        annotations_data = cursor.fetchall()
        
        # 写入 CSV 文件
        for data in annotations_data:
            csv_writer.writerow([data[0], data[1], data[2], data[3], data[4], data[5], data[6]])

# 关闭游标和连接
cursor.close()
conn.close()



# 定义颜色映射
color_mapping = {
    '#ffd400': 'yellow',
    '#ff6666': 'red',
    '#5fb236': 'green',
    '#2ea8e5': 'blue',
    '#a28ae5': 'purple',
    '#e56eee': 'magenta',
    '#f19837': 'orange',
    '#aaaaaa': 'gray'
}

# 定义type映射
type_mapping = {
    '1': 'highlight',
    '2': 'note',
    '3': 'selection'
}


# 读取CSV文件
with open(input_csv_path, mode='r', newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    rows = [row for row in csv_reader]

    # 按parentItemID分组
    grouped_by_parent_item_id = {}
    for row in rows:
        parent_item_id = row['parentItemID']
        if parent_item_id not in grouped_by_parent_item_id:
            grouped_by_parent_item_id[parent_item_id] = []
        grouped_by_parent_item_id[parent_item_id].append(row)



with open(output_md_path, mode='w', encoding='utf-8') as mdfile, \
     open(output_new_csv_path, mode='w', newline='', encoding='utf-8') as new_csvfile:
    
    # Markdown文件的表头
    md_table_header = "| Color | Text | Comment | Page | Type |\n"
    md_table_separator = "|-------|------|---------|----------|------|\n"
    
    # 写入Markdown文件的表头
    # mdfile.write(md_table_header)
    # mdfile.write(md_table_separator)
    
    csv_writer = csv.writer(new_csvfile)
    # 写入新的CSV文件的表头
    csv_writer.writerow(['Color', 'Text', 'Comment', 'Page', 'Type'])

    # 初始化表格计数器
    table_counter = 1

    # 遍历每个parentItemID及其对应的行
    for parent_item_id, rows in grouped_by_parent_item_id.items():
        # 为每个parentItemID创建一个Markdown表格
        mdfile.write(f"## Table {table_counter}\n")
        mdfile.write(md_table_header)
        mdfile.write(md_table_separator)
        
        for row in rows:
            # 处理type和color列
            original_color = row['color']
            processed_color = color_mapping.get(row['color'], 'unknown')
            processed_type = type_mapping.get(row['type'], 'unknown')
            
            # 写入Markdown文件
            mdfile.write(f"| <font color={original_color}>**{processed_color}**</font> | {row['text']} | {row['comment']} | {row['pagelabel']} | **{processed_type}** |\n")
            
            # 写入新的CSV文件，注意这里不需要HTML标签
            csv_writer.writerow([processed_color, row['text'], row['comment'], row['pagelabel'], processed_type])
        
        # 递增表格计数器
        table_counter += 1

print("Markdown file and new CSV file have been created successfully.")