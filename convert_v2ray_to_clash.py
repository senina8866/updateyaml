import requests

# 配置部分
raw_file_url = "https://raw.githubusercontent.com/senina8866/updateyaml/refs/heads/main/configs/config3.txt"
output_file_path = "./configs/config3.yaml"
conversion_url = "https://v1.v2rayse.com/v2ray-clash/"

def download_config(file_url):
    """从 GitHub 下载配置内容"""
    response = requests.get(file_url, timeout=10)
    if response.status_code == 200:
        print("配置文件内容下载成功！")
        return response.text  # 返回文件内容
    else:
        raise Exception(f"下载失败，状态码: {response.status_code}")

def convert_config_to_yaml(config_content):
    """将配置内容提交到在线工具并转换"""
    data = {"text": config_content}  # 提交内容作为文本
    response = requests.post(conversion_url, data=data, timeout=10)
    if response.status_code == 200:
        print("转换成功！")
        if "port:" in response.text:  # 校验 YAML 格式
            return response.text
        else:
            raise Exception("返回结果可能不是有效的 YAML 格式！")
    else:
        raise Exception(f"转换失败，状态码: {response.status_code}")

def save_to_file(content, file_path):
    """将转换结果保存为 YAML 文件"""
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"文件已保存到: {file_path}")

# 主逻辑
try:
    # 步骤 1: 下载文件内容
    print("开始下载配置文件内容...")
    config_content = download_config(raw_file_url)

    # 步骤 2: 将内容提交到转换工具
    print("开始提交内容并转换...")
    yaml_content = convert_config_to_yaml(config_content)

    # 步骤 3: 保存 YAML 文件
    print("开始保存 YAML 文件...")
    save_to_file(yaml_content, output_file_path)

    print("任务完成！配置已成功转换并保存为 YAML 格式。")

except Exception as e:
    print(f"发生错误: {e}")
