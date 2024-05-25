from tkinter import Tk, Label, Entry, Button, Text, Frame

# 新增更多数据类型的编码函数
def ber_encode(data_type, value):
    if data_type == 'Integer':
        encoded_value = value.to_bytes(4, byteorder='big')
        return encoded_value
    elif data_type == 'OCTET STRING':
        return value.encode()
    elif data_type == 'BOOLEAN':
        if value.lower() == 'true':
            return b'\x01'
        elif value.lower() == 'false':
            return b'\x00'
    elif data_type == 'REAL':  # 假设简单表示浮点数
        return value.encode()
    elif data_type == 'get':
        # 详细表示
        encoded_value = b'\x00\x01' + b'GET'
        return encoded_value

# 对应更多数据类型的解码函数
def ber_decode(encoded_data):
    if len(encoded_data) == 4:
        decoded_value = int.from_bytes(encoded_data, byteorder='big')
        return 'Integer', decoded_value
    elif encoded_data.startswith(b'\x00'):
        if encoded_data == b'\x00':
            return 'BOOLEAN', 'False'
        elif encoded_data == b'\x01':
            return 'BOOLEAN', 'True'
    elif encoded_data.startswith(b'\x00\x01GET'):
        return 'get', 'GET 操作'
    elif encoded_data.startswith(b'\x04'):  # 假设表示 OCTET STRING
        return 'OCTET STRING', encoded_data[1:]
    elif encoded_data.startswith(b'\x08'):  # 假设表示 REAL
        return 'REAL', float(encoded_data[1:].decode())
    else:
        decoded_value = encoded_data.decode()
        return 'Other', '其他类型数据'

class BERCodecGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("BER 编解码器")

        main_frame = Frame(self.root)
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)

        self.label_type = Label(main_frame, text="数据类型:")
        self.label_type.grid(row=0, column=0)

        self.entry_type = Entry(main_frame)
        self.entry_type.grid(row=0, column=1)

        self.label_value = Label(main_frame, text="值:")
        self.label_value.grid(row=1, column=0)

        self.entry_value = Entry(main_frame)
        self.entry_value.grid(row=1, column=1)

        self.encode_button = Button(main_frame, text="编码", command=self.encode)
        self.encode_button.grid(row=2, column=0)

        self.decode_button = Button(main_frame, text="解码", command=self.decode)
        self.decode_button.grid(row=2, column=1)

        self.result_label = Label(main_frame, text="")
        self.result_label.grid(row=3, column=0, columnspan=2)

        self.text_area = Text(main_frame, height=20, width=80)
        self.text_area.grid(row=4, column=0, columnspan=2, pady=10)

    def encode(self):
        data_type = self.entry_type.get()
        value = self.entry_value.get()
        encoded_data = ber_encode(data_type, value)
        self.text_area.insert("end", f"编码数据类型: {data_type}\n")
        self.text_area.insert("end", f"编码前的值: {value}\n")
        self.text_area.insert("end", f"编码结果: {encoded_data}\n")

    def decode(self):
        encoded_data = self.entry_value.get().encode()
        data_type, decoded_value = ber_decode(encoded_data)
        self.text_area.insert("end", f"解码数据类型: {data_type}\n")
        self.text_area.insert("end", f"解码结果: {data_type} - {decoded_value}\n")

if __name__ == "__main__":
    gui = BERCodecGUI()
    gui.root.mainloop()