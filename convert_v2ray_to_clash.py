import yaml
import requests

# 从 v2ray 配置文件的 URL 下载内容
def download_v2ray_config(url):
    response = requests.get(url)
    response.raise_for_status()  # 如果请求失败，会抛出异常
    return response.text

# 将 v2ray 配置转换为 clash 配置
def convert_v2ray_to_clash(v2ray_config):
    clash_config = {
        'proxies': [],
        'proxy-groups': [],
        'rules': [],
    }

    # 假设配置内容是 JSON 或 YAML 格式的，我们需要提取代理信息
    # 此处假设 v2ray 配置是简单的文本信息，每个代理节点以 "server" 字段开头

    # 根据你提供的文件内容进行解析（这里我假设是纯文本，可以按需调整）
    lines = v2ray_config.splitlines()
    for line in lines:
        if "server" in line:
            # 提取代理节点信息
            # 假设代理节点的格式是 "server = xxx, port = xxx" 这种形式
            parts = line.split(',')
            server = parts[0].split('=')[1].strip()  # 获取服务器地址
            port = parts[1].split('=')[1].strip()  # 获取端口

            # 这里需要根据实际的 v2ray 配置提取 UUID、alterId 等信息
            # 假设 v2ray 配置文件内的 UUID 和 alterId 也有类似的字段

            proxy = {
                'name': f'V2Ray-{server}',
                'type': 'vmess',  # 假设是 vmess 类型
                'server': server,
                'port': int(port),
                'uuid': 'xxxx-xxxx-xxxx-xxxx',  # 需要从配置中提取实际的 UUID
                'alterId': 64,  # 假设值
                'cipher': 'auto',  # 需要调整为合适的值
                'tls': True,  # 假设启用 TLS
            }

            clash_config['proxies'].append(proxy)

    # 添加一些默认规则，实际需要根据需求来定制
    clash_config['rules'] = [
        'DOMAIN-SUFFIX,google.com,PROXY',
        'DOMAIN-KEYWORD,apple,PROXY',
        'MATCH,DIRECT'
    ]
    
    return clash_config

# 将转换后的数据写入到 clash 配置文件
def save_clash_config(file_path, clash_config):
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.dump(clash_config, file, allow_unicode=True)

# 主函数
def main():
    v2ray_url = 'https://raw.githubusercontent.com/senina8866/updateyaml/refs/heads/main/configs/config3.txt'
    clash_file_path = './configs/config3.yaml'

    # 从 URL 下载 v2ray 配置
    v2ray_config = download_v2ray_config(v2ray_url)

    # 转换 v2ray 配置为 clash 配置
    clash_config = convert_v2ray_to_clash(v2ray_config)

    # 保存 clash 配置
    save_clash_config(clash_file_path, clash_config)

    print(f"Clash 配置已保存至 {clash_file_path}")

# 运行程序
if __name__ == '__main__':
    main()
