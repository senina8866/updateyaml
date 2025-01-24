import yaml

def merge_yaml(file1, file2):
    """合并两个YAML文件。

    Args:
      file1: 第一个YAML文件的路径。
      file2: 第二个YAML文件的路径。

    Returns:
      合并后的YAML内容字符串。
    """
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        try:
            data1 = yaml.safe_load(f1)
            data2 = yaml.safe_load(f2)
        except yaml.YAMLError as e:
            print(f"YAML文件加载错误: {e}")
            return None

    # 合并proxies
    data1['proxies'].extend(data2['proxies'])

    # 合并proxy-groups
    for group2 in data2['proxy-groups']:
        name2 = group2['name']
        found = False
        for group1 in data1['proxy-groups']:
            if group1['name'] == name2:
                group1['proxies'].extend(group2['proxies'])
                found = True
                break
        if not found:
            data1['proxy-groups'].append(group2)

    # 合并rules
    data1['rules'].extend(data2['rules'])

    # 返回合并后的YAML字符串
    return yaml.dump(data1, allow_unicode=True, sort_keys=False)

if __name__ == "__main__":
    file1 = './configs/config1.yaml'  # 确保路径是正确的
    file2 = './configs/config2.yaml'
    merged_yaml = merge_yaml(file1, file2)
    if merged_yaml:
        # 直接写入到 configs 文件夹
        with open('./configs/config_merged.yaml', 'w', encoding='utf-8') as f:
            f.write(merged_yaml)
        print("YAML文件合并完成，已保存到 ./configs/config_merged.yaml")
    else:
        print("YAML合并失败")
