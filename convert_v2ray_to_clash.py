import base64
import yaml
import re
from urllib.parse import unquote

# 解析 ss:// 格式
def parse_ss(url):
    match = re.match(r"ss://([a-zA-Z0-9+/=]+)@([a-zA-Z0-9.-]+):(\d+)(#.*)?", url)
    if match:
        encoded_password = match.group(1)
        server = match.group(2)
        port = match.group(3)
        name = unquote(match.group(4)[1:]) if match.group(4) else server

        password = base64.urlsafe_b64decode(encoded_password + '==').decode('utf-8')
        return {
            "name": name,
            "type": "ss",
            "server": server,
            "port": int(port),
            "cipher": "aes-256-gcm",  # 默认加密方式
            "password": password,
            "tls": False  # 默认禁用TLS，除非明确指定
        }
    return None

# 解析 vmess:// 格式
def parse_vmess(url):
    match = re.match(r"vmess://([a-zA-Z0-9+/=]+)", url)
    if match:
        decoded = base64.urlsafe_b64decode(match.group(1) + '==').decode('utf-8')
        config = yaml.safe_load(decoded)

        return {
            "name": config["ps"],
            "type": "vmess",
            "server": config["add"],
            "port": config["port"],
            "uuid": config["id"],
            "alterId": config["aid"],
            "cipher": "auto",
            "tls": True if config["tls"] == "true" else False  # 确保TLS字段是布尔类型
        }
    return None

# 解析 trojan:// 格式
def parse_trojan(url):
    match = re.match(r"trojan://([a-zA-Z0-9]+)@([a-zA-Z0-9.-]+):(\d+)\?([^\s]+)(#.*)?", url)
    if match:
        password = match.group(1)
        server = match.group(2)
        port = match.group(3)
        options = match.group(4)
        name = unquote(match.group(5)[1:]) if match.group(5) else server

        return {
            "name": name,
            "type": "trojan",
            "server": server,
            "port": int(port),
            "password": password,
            "tls": True  # 默认启用TLS
        }
    return None

# 读取配置文件并转换
def convert_v2ray_to_clash(input_file, output_file):
    proxies = []

    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            if not line:
                continue

            if line.startswith('ss://'):
                proxy = parse_ss(line)
            elif line.startswith('vmess://'):
                proxy = parse_vmess(line)
            elif line.startswith('trojan://'):
                proxy = parse_trojan(line)
            else:
                continue

            if proxy:
                proxies.append(proxy)

    # 构建Clash配置
    clash_config = {
        'proxies': proxies,
        'proxy-groups': [],
        'rules': [
            # 示例规则
            {"type": "field", "domain": "google.com", "outboundTag": "Proxy"},
            {"type": "field", "ip": "8.8.8.8", "outboundTag": "Proxy"},
            {"type": "field", "domain": "youtube.com", "outboundTag": "Proxy"},
            {"type": "final", "outboundTag": "DIRECT"}
        ]
    }

    # 输出Clash配置
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(clash_config, f, default_flow_style=False, allow_unicode=True)

    print(f"Clash配置已保存至 {output_file}")

# 执行转换
input_file = './configs/config3.txt'  # 输入V2Ray配置文件
output_file = './configs/config3.yaml'  # 输出Clash配置文件
convert_v2ray_to_clash(input_file, output_file)
