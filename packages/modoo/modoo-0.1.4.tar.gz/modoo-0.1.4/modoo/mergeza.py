# built-ins
import json
import os
# third-parties
from openpyxl import Workbook
# customs
from modoo.zafuncs import compare_num_za, merge_docs, fold_docs


def run(za_s_file_path, za_o_file_path, new_file_id):

    title_map = {'N': '신문', 'S': '구어'}
    title_type = title_map[new_file_id[0]]
    new_file_title = f'국립국어원 {title_type} 말뭉치 추출 {new_file_id}'
    merged_file_name = f'./out/{new_file_id}.json'
    num_check_file_name = f'./out/{new_file_id}.za_num.xlsx'

    print(f'read: {za_s_file_path}')
    with open(za_s_file_path, 'r', encoding='utf8') as file:
        za_s_data = json.load(file)

    print(f'read: {za_o_file_path}')
    with open(za_o_file_path, 'r', encoding='utf8') as file:
        za_o_data = json.load(file)

    za_s_docs = za_s_data['document']
    za_o_docs = za_o_data['document']

    print('process: merge ZA')
    za_so_docs = merge_docs(za_s_docs, za_o_docs)

    print('process: fold & sort ZA')
    za_docs = fold_docs(za_so_docs)

    metadata = {**za_o_data['metadata'], 'title': new_file_title}

    merged = {'id': new_file_id, 'metadata': metadata, 'document': za_docs}

    os.makedirs('./out', exist_ok=True)

    print(f'write: {merged_file_name}')

    with open(merged_file_name, 'w', encoding='utf8') as file:
        json.dump(merged, file, indent=4, ensure_ascii=False)

    wb = Workbook()
    ws = wb.active

    for row in compare_num_za(za_s_docs, za_o_docs, za_so_docs, za_docs):
        ws.append(row)

    print(f'write: {num_check_file_name}')

    wb.save(num_check_file_name)
    print('DONE!!')
