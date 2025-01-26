import yaml
import re
import base64
import json

def decode_v2ray_url(v2ray_url):
    if v2ray_url.startswith('vless://'):
        pattern = r'vless://(?P<uuid>[^@]+)@(?P<address>[^:]+):(?P<port>\d+)\?(?P<params>[^#]+)#(?P<name>.+)'
        match = re.match(pattern, v2ray_url)
        if not match:
            raise ValueError("Invalid V2Ray URL format")
        params_str = match.group('params')
        params = {}
        for pair in params_str.split('&'):
            if '=' in pair:
                key, value = pair.split('=', 1)
                params[key] = value
            else:
                params[pair] = None
        # 将alpn转换为列表
        alpn_list = params.get('alpn', '').split(',') if 'alpn' in params else []
        return {
            'name': match.group('name'),
            'type': 'vless',
            'server': match.group('address'),
            'port': int(match.group('port')),
            'uuid': match.group('uuid'),
            'security': params.get('security', 'none'),
            'sni': params.get('sni', ''),
            'alpn': alpn_list,
            'network': params.get('type', 'tcp'),
            'headers': {
                'type': params.get('headerType', 'none')
            }
        }
    elif v2ray_url.startswith('vmess://'):
        decoded_json = base64.b64decode(v2ray_url[8:]).decode('utf-8')
        data = json.loads(decoded_json)
        return {
            'name': data['ps'],
            'type': 'vmess',
            'server': data['add'],
            'port': int(data['port']),
            'uuid': data['id'],
            'alterId': int(data['aid']),
            'cipher': 'auto',
            'tls': data.get('tls', 'none'),
            'network': data.get('net', 'tcp'),
            'ws-opts': {
                'path': data.get('path', ''),
                'headers': {
                    'Host': data.get('host', '')
                }
            }
        }
    elif v2ray_url.startswith('trojan://'):
        pattern = r'trojan://(?P<password>[^@]+)@(?P<address>[^:]+):(?P<port>\d+)\?(?P<params>[^#]+)#(?P<name>.+)'
        match = re.match(pattern, v2ray_url)
        if not match:
            raise ValueError("Invalid Trojan URL format")
        params_str = match.group('params')
        params = {}
        for pair in params_str.split('&'):
            if '=' in pair:
                key, value = pair.split('=', 1)
                params[key] = value
            else:
                params[pair] = None
        return {
            'name': match.group('name'),
            'type': 'trojan',
            'server': match.group('address'),
            'port': int(match.group('port')),
            'password': match.group('password'),
            'sni': params.get('sni', ''),
            'alpn': params.get('alpn', '').split(',') if 'alpn' in params else [],
            'network': 'tcp',
            'tls': 'true'
        }
    else:
        raise ValueError("Unsupported V2Ray URL type")

def save_as_yaml(proxies, output_file, rules, groups):
    clash_config = {
        'proxies': proxies,
        'proxy-groups': groups,
        'rules': rules
    }
    with open(output_file, 'w') as f:
        yaml.dump(clash_config, f, allow_unicode=True)

if __name__ == "__main__":
    with open('./configs/config3.txt', 'r') as f:
        v2ray_urls = f.read().splitlines()

    proxies = [decode_v2ray_url(url) for url in v2ray_urls if url.startswith(("vless://", "vmess://", "trojan://"))]

    rules = [
        'RULE-SET,https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Lan/Lan.list,🎯 全球直连',
        'RULE-SET,https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Direct/Direct.list,🎯 全球直连',
        'RULE-SET,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/BanAD.list,🛑 全球拦截',
        'RULE-SET,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/BanProgramAD.list,🍃 应用净化',
        'RULE-SET,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/GoogleCN.list,🎯 全球直连',
        'RULE-SET,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/SteamCN.list,🎯 全球直连',
        'RULE-SET,https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Bing/Bing.list,Ⓜ️ Copilot',
        'RULE-SET,https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Copilot/Copilot.list,Ⓜ️ Copilot'
    ]
    rules.extend([
        'RULE-SET,https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Microsoft/Microsoft.list,Ⓜ️ 微软服务',
        'RULE-SET,https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Apple/Apple.list,🍎 苹果服务',
        'RULE-SET,https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Telegram/Telegram.list,📲 Telegram',
        'RULE-SET,https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/OpenAI/OpenAI.list,💬 OpenAi',
        'RULE-SET,https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Claude/Claude.list,💬 OpenAi',
        'RULE-SET,https://raw.githubusercontent.com/coco-yan/proxy_ruleset/dev/rule_addition.list,💬 OpenAi',
        'RULE-SET,https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Netflix/Netflix.list,🎥 Netflix',
        'RULE-SET,https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/GlobalMedia/GlobalMedia.list,🌍 国外媒体',
        'RULE-SET,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ProxyLite.list,🚀 节点选择',
        'RULE-SET,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ChinaDomain.list,🎯 全球直连',
        'RULE-SET,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ChinaCompanyIp.list,🎯 全球直连',
        'RULE-SET,https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Download/Download.list,🎯 全球直连',
        'GEOIP,CN,🎯 全球直连',
        'FINAL,🐟 漏网之鱼'
    ])

    groups = [
        {
            'name': '🚀 节点选择',
            'type': 'select',
            'proxies': ['DIRECT'] + [proxy['name'] for proxy in proxies]
        },
        {
            'name': '🚀 手动切换',
            'type': 'select',
            'proxies': ['♻️ Auto'] + [proxy['name'] for proxy in proxies]
        },
        {
            'name': '♻️ Auto',
            'type': 'select',
            'proxies': ['DIRECT'] + [proxy['name'] for proxy in proxies]
        },
        {
            'name': '🌍 国外媒体',
            'type': 'select',
            'proxies': ['DIRECT'] + [proxy['name'] for proxy in proxies]
        }
    ]
    save_as_yaml(proxies, './configs/config3.yaml', rules, groups)
    print("转换完成，并保存为 ./configs/config3.yaml")
