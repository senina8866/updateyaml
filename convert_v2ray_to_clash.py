# 段落1
import base64
import yaml

# 解析V2Ray TXT的各个部分并转换为Clash YAML格式
def parse_v2ray_txt(input_file, output_file):
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

    config = {
        'proxies': proxies,
        'proxy-groups': [
            {
                'name': 'Auto',
                'type': 'url-test',
                'proxies': [proxy['name'] for proxy in proxies],
                'url': 'http://www.google.com/generate_204',
                'interval': 300
            }
        ]
    }

    with open(output_file, 'w') as f:
        yaml.dump(config, f, allow_unicode=True)

# 解析SS协议
def parse_ss(url):
    decoded = base64.urlsafe_b64decode(url[5:]).decode('utf-8')
    parts = decoded.split('@')
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
# 段落2
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
    data = base64.urlsafe_b64decode(url[8:]).decode('utf-8')
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
# 段落3
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
    parse_v2ray_txt(input_path, output_path)
