import yaml
import re

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
    # 读取解码后的内容，并解析为 Clash 格式
    with open('./configs/config3.txt', 'r') as f:
        v2ray_urls = f.read().splitlines()

    # 打印解码后的内容以进行调试
    print("解码后的 V2Ray URL 内容：")
    for url in v2ray_urls:
        print(url)

    # 解析并转换 V2Ray URL
    proxies = [decode_v2ray_url(url) for url in v2ray_urls if url.startswith("vless://")]
    save_as_yaml(proxies, './configs/config3.yaml')
    print("转换完成，并保存为 ./configs/config3.yaml")
