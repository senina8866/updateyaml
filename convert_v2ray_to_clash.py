import os
import yaml
import logging

# 初始化日志
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

# 全局变量
CONFIG_DIR = './configs'
INPUT_FILE = os.path.join(CONFIG_DIR, 'config4.txt')
OUTPUT_FILE = os.path.join(CONFIG_DIR, 'clash_config.yaml')
NET_CONFIG = 'https://raw.githubusercontent.com/Roiocam/V2ray2Clash/master/config.yaml'


def log(msg):
    logging.info(msg)


def save_to_file(file_name, contents):
    with open(file_name, 'w', encoding="utf-8") as fh:
        fh.write(contents)


def get_github_config():
    try:
        import urllib.request
        HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/87.0.4280.141 Safari/537.36"}
        req = urllib.request.Request(url=NET_CONFIG, headers=HEADERS)
        raw = urllib.request.urlopen(req).read().decode('utf-8')
        return yaml.safe_load(raw)
    except Exception as e:
        log(f'网络获取规则配置失败: {e}')
        exit()


def load_local_config():
    try:
        with open(INPUT_FILE, 'r', encoding="utf-8") as f:
            return yaml.safe_load(f.read())
    except FileNotFoundError:
        log('本地配置文件加载失败')
        exit()


def add_proxies_to_config(data, config):
    config['proxies'] = data['proxies']
    for group in config.get('proxy-groups', []):
        if group.get('proxies') is None:
            group['proxies'] = [proxy['name'] for proxy in data['proxies']]
        elif 'DIRECT' == group['proxies'][0]:
            continue
        else:
            group['proxies'].extend([proxy['name'] for proxy in data['proxies']])
    return config


def save_config(config_data):
    length = len(config_data['proxies'])
    config_yaml = yaml.dump(config_data, sort_keys=False, default_flow_style=False, allow_unicode=True)
    save_to_file(OUTPUT_FILE, config_yaml)
    log(f'成功更新 {length} 个节点')


# 程序入口
if __name__ == "__main__":
    local_config = load_local_config()
    github_config = get_github_config()
    updated_config = add_proxies_to_config(local_config, github_config)
    save_config(updated_config)
