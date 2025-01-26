import base64

def decode_base64_file(input_file):
    with open(input_file, 'r') as f:
        encoded_content = f.read()
    decoded_content = base64.b64decode(encoded_content).decode('utf-8')
    return decoded_content

def main():
    files = ['./configs/config1.txt', './configs/config2.txt', './configs/config3.txt']
    decoded_contents = []

    # 解码三个文件的内容
    for file in files:
        decoded_contents.append(decode_base64_file(file))

    # 合并解码后的内容
    merged_content = "\n".join(decoded_contents)

    # 将合并后的内容写入 config4.txt
    with open('./configs/config4.txt', 'w') as f:
        f.write(merged_content)

    print("已将解码并合并的内容写入 config4.txt")

if __name__ == "__main__":
    main()
