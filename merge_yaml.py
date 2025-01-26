import os
import yaml

def merge_yaml(file1, file2, file3):
    if not os.path.exists(file1) or not os.path.exists(file2) or not os.path.exists(file3):
        print("一个或多个文件路径无效")
        return None

    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2, open(file3, 'r', encoding='utf-8') as f3:
        try:
            data1 = yaml.safe_load(f1)
            data2 = yaml.safe_load(f2)
            data3 = yaml.safe_load(f3)
        except yaml.YAMLError as e:
            print(f"YAML文件加载错误: {e}")
            return None

    # 确保键存在
    for key in ['proxies', 'proxy-groups', 'rules']:
        if key not in data1:
            data1[key] = []
        if key not in data2:
            data2[key] = []
        if key not in data3:
            data3[key] = []

    # 合并并去重proxies
    data1['proxies'] = list({v['name']:v for v in data1['proxies'] + data2['proxies'] + data3['proxies']}.values())

    # 合并并去重proxy-groups
    group_dict = {group['name']: group for group in data1['proxy-groups']}
    for group in data2['proxy-groups'] + data3['proxy-groups']:
        name = group['name']
        if name in group_dict:
            existing_group = group_dict[name]
            existing_group['proxies'] = list(set(existing_group['proxies'] + group['proxies']))
        else:
            group_dict[name] = group
    data1['proxy-groups'] = list(group_dict.values())

    # 合并并去重rules
    data1['rules'] = list(set(data1['rules'] + data2['rules'] + data3['rules']))

    return yaml.dump(data1, allow_unicode=True, sort_keys=False)

if __name__ == "__main__":
    file1 = './configs/config1.yaml'
    file2 = './configs/config2.yaml'
    file3 = './configs/config3.yaml'
    merged_yaml = merge_yaml(file1, file2, file3)
    if merged_yaml:
        with open('./configs/config_merged.yaml', 'w', encoding='utf-8') as f:
            f.write(merged_yaml)
        print("YAML文件合并完成，已保存到 ./configs/config_merged.yaml")
    else:
        print("YAML合并失败")
