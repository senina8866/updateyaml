import os
import urllib.request
import base64
import json
import datetime
import yaml
import logging

# 初始化日志
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

# 全局变量
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/87.0.4280.141 Safari/537.36"}
URL = 'https://dy.wmyun.men/link/LET56VNfZlrUwKtg?mu=2'
CONFIG_DIR = './configs'
INPUT_FILE = os.path.join(CONFIG_DIR, 'config4.txt')
OUTPUT_FILE = os.path.join(CONFIG_DIR, 'clash_config.yaml')
NET_CONFIG = 'https://raw.githubusercontent.com/Roiocam/V2ray2Clash/master/config.yaml'


def log(msg):
    logging.info(msg)


def save_to_file(file_name, contents):
    with open(file_name, 'w', encoding="utf-8") as fh:
        fh.write(contents)


def get_proxies(url):
    proxies = []
    try:
        req = urllib.request.Request(url=url, headers=HEADERS)
        raw = urllib.request.urlopen(req).read().decode('utf-8')
        vmess_raw = base64.b64decode(raw.replace("\n", ""))
        vmess_list = vmess_raw.splitlines()
        log(f'已获取 {len(vmess_list)} 个节点')
        for item in vmess_list:
            try:
                b64_proxy = item.decode('utf-8')[8:]
                proxy_str = base64.b64decode(b64_proxy).decode('utf-8')
                proxies.append(proxy_str)
            except Exception as e:
                log(f"解析代理失败: {e}")
    except Exception as e:
        log(f"获取订阅失败: {e}")
    return proxies


def translate_proxy(arr):
    log('代理节点转换中...')
    proxies = {'proxy_list': [], 'proxy_names': []}
    for temp in arr:
        try:
            item = json.loads(temp)
            if 'tls' not in item:
                continue
            obj = {
                'name': item.get('ps'),
                'type': 'vmess',
                'server': item.get('add'),
                'port': item.get('port'),
                'uuid': item.get('id'),
                'alterId': item.get('aid'),
                'cipher': 'auto' if item.get('type') == 'none' else None,
                'network': item.get('net'),
                'ws-path': item.get('path'),
                'ws-headers': {'Host': item.get('host')},
                'tls': item.get('tls') == 'tls',
            }
            obj = {k: v for k, v in obj.items() if v is not None}
            proxies['proxy_list'].append(obj)
            proxies['proxy_names'].append(obj['name'])
        except Exception as e:
            log(f"转换节点失败: {e}")
    return proxies


def get_github_config():
    try:
        req = urllib.request.Request(url=NET_CONFIG, headers=HEADERS)
        raw = urllib.request.urlopen(req).read().decode('utf-8')
        return yaml.safe_load(raw)
    except Exception as e:
        log(f'网络获取规则配置失败: {e}')
        exit()


def add_proxies_to_config(data, config):
    config['proxies'] = data['proxy_list']
    for group in config.get('proxy-groups', []):
        if group.get('proxies') is None:
            group['proxies'] = data['proxy_names']
        elif 'DIRECT' == group['proxies'][0]:
            continue
        else:
            group['proxies'].extend(data['proxy_names'])
    return config


def save_config(config_data):
    length = len(config_data['proxies'])
    config_yaml = yaml.dump(config_data, sort_keys=False, default_flow_style=False, allow_unicode=True)
    save_to_file(OUTPUT_FILE, config_yaml)
    log(f'成功更新 {length} 个节点')


# 程序入口
if __name__ == "__main__":
    config_raw = get_github_config()
    proxy_raw = get_proxies(URL)
    proxy = translate_proxy(proxy_raw)
    config = add_proxies_to_config(proxy, config_raw)
    save_config(config)
