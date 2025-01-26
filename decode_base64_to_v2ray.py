import base64

def decode_base64_file(input_file, output_file):
    with open(input_file, 'r') as f:
        encoded_content = f.read()
    decoded_content = base64.b64decode(encoded_content).decode('utf-8')
    with open(output_file, 'w') as f:
        f.write(decoded_content)
    print("解码后的内容：")
    print(decoded_content)

if __name__ == "__main__":
    decode_base64_file('./configs/config3-base64.txt', './configs/config3.txt')
