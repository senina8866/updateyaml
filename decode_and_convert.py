import base64
import yaml
import re

def decode_base64_file(input_file, output_file):
    with open(input_file, 'r') as f:
        encoded_content = f.read()
    decoded_content = base64.b64decode(encoded_content).decode('utf-8')
    with open(output_file, 'w') as f:
        f.write(decoded_content)

def decode_v2ray_url(v2ray_url):
    pattern = r'vless://(?P<uuid>[^@]+)@(?P<address>[^:]+):(?P<port>\d+)\?(?P<params>[^#]+)#(?P<name>.+)'
    match = re.match(pattern, v2ray_url)
    if not match:
        raise ValueError("Invalid V2Ray URL format")

    params = dict(pair.split('=') for pair in match.group('params').split('&'))
    clash_proxy = {
        'name': match.group('name'),
        'type': 'vless',
        'server': match.group('address'),
        'port': int(match.group('port')),
        'uuid': match.group('uuid'),
        'security': params.get('security', 'none'),
        'sni': params.get('sni', ''),
        'alpn': params.get('alpn', ''),
        'network': params.get('type', 'tcp'),
        'headers': {
            'type': params.get('headerType', 'none')
        }
    }
    return clash_proxy

def save_as_yaml(proxies, output_file):
    clash_config = {'proxies': proxies}
    with open(output_file, 'w') as f:
        yaml.dump(clash_config, f, allow_unicode=True)

if __name__ == "__main__":
    # 先解码 Base64 编码的 TXT 文件
    decode_base64_file('./configs/config3.txt', './configs/config3_decoded.txt')

    # 读取解码后的内容，并解析为 Clash 格式
    with open('./configs/config3_decoded.txt', 'r') as f:
        v2ray_urls = f.read().splitlines()

    proxies = [decode_v2ray_url(url) for url in v2ray_urls]
    save_as_yaml(proxies, './configs/config3.yaml')
    print("转换完成，并保存为 ./configs/config3.yaml")
