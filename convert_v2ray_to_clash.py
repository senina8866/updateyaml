import base64
import yaml
import requests

# 解析V2Ray TXT文件并转换为Clash YAML格式
def convert_v2ray_to_clash(input_file, output_file, rule_url):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    proxies = []

    for line in lines:
        line = line.strip()
        if line.startswith('ss://'):
            proxies.append(parse_ss(line))
        elif line.startswith('trojan://'):
            proxies.append(parse_trojan(line))
        elif line.startswith('vmess://'):
            proxies.append(parse_vmess(line))
        elif line.startswith('vless://'):
            proxies.append(parse_vless(line))

    clash_config = {
        'proxies': proxies,
        'proxy-groups': [
            {
                'name': 'Auto',
                'type': 'url-test',
                'proxies': [proxy['name'] for proxy in proxies],
                'url': 'http://www.google.com/generate_204',
                'interval': 300
            }
        ],
        'rules': fetch_rules(rule_url)
    }

    with open(output_file, 'w') as f:
        yaml.dump(clash_config, f, allow_unicode=True)

# 获取规则集
def fetch_rules(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text.splitlines()
    except Exception as e:
        print(f"Failed to fetch rules from {url}: {e}")
        return []

# 解析SS协议
def parse_ss(url):
    base64_data = url[5:].split('#')[0]  # 去掉标签部分
    # 确保 Base64 长度是 4 的倍数
    padding = 4 - (len(base64_data) % 4)
    if padding and padding < 4:
        base64_data += '=' * padding

    try:
        decoded = base64.urlsafe_b64decode(base64_data).decode('utf-8')
    except Exception as e:
        raise ValueError(f"Failed to decode SS URL: {url}. Error: {e}")
    
    parts = decoded.split('@')
    if len(parts) != 2:
        raise ValueError(f"Invalid SS URL format: {decoded}")
    
    method_password, server_port = parts[0], parts[1]
    method, password = method_password.split(':')
    server, port = server_port.split(':')

    return {
        'name': 'SS-' + server,
        'type': 'ss',
        'server': server,
        'port': int(port),
        'cipher': method,
        'password': password
    }

# 解析Trojan协议
def parse_trojan(url):
    main_part, params = url[9:].split('?', 1)
    user_pass, server_port = main_part.split('@')
    username, password = user_pass.split(':')
    server, port = server_port.split(':')

    param_dict = dict(param.split('=') for param in params.split('&'))

    return {
        'name': 'Trojan-' + server,
        'type': 'trojan',
        'server': server,
        'port': int(port),
        'password': username,
        'sni': param_dict.get('sni', ''),
        'network': param_dict.get('type', 'tcp'),
        'ws-opts': {
            'path': param_dict.get('path', ''),
            'headers': {
                'Host': param_dict.get('host', '')
            }
        }
    }

# 解析VMess协议
def parse_vmess(url):
    base64_data = url[8:]
    data = base64.urlsafe_b64decode(base64_data).decode('utf-8')
    vmess_config = yaml.safe_load(data)

    return {
        'name': 'VMess-' + vmess_config['add'],
        'type': 'vmess',
        'server': vmess_config['add'],
        'port': int(vmess_config['port']),
        'uuid': vmess_config['id'],
        'alterId': vmess_config.get('aid', 0),
        'cipher': vmess_config.get('scy', 'auto'),
        'network': vmess_config['net'],
        'tls': vmess_config.get('tls', False)
    }

# 解析VLESS协议
def parse_vless(url):
    main_part, params = url[8:].split('?', 1)
    uuid_server, server_port = main_part.split('@')
    uuid, server = uuid_server.split(':')
    port = server_port.split(':')[1]

    param_dict = dict(param.split('=') for param in params.split('&'))

    return {
        'name': 'VLESS-' + server,
        'type': 'vless',
        'server': server,
        'port': int(port),
        'uuid': uuid,
        'tls': param_dict.get('security', '') == 'tls',
        'network': param_dict.get('type', 'tcp'),
        'ws-opts': {
            'path': param_dict.get('path', ''),
            'headers': {
                'Host': param_dict.get('sni', '')
            }
        }
    }

if __name__ == "__main__":
    input_path = "./configs/config3.txt"
    output_path = "./configs/config3.yaml"
    rule_url = "https://raw.githubusercontent.com/Semporia/Clash/refs/heads/master/Calsh%20for%20Windows/config.yaml"
    convert_v2ray_to_clash(input_path, output_path, rule_url)
