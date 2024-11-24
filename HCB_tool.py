from Lib import *
from HCB_OP import *
from io import BytesIO

class HCB_Reader(BytesIO):
    def readU32(self):
        res = self.read(4)
        res = from_bytes(res)
        return res
    
    def readU16(self):
        res = self.read(2)
        res = from_bytes(res)
        return res
    
    def readU8(self):
        res = self.read(1)
        res = from_bytes(res)
        return res

    def set_encoding(self, encoding):
        self.encoding = encoding

    def readString(self):
        length = from_bytes(self.read(1))
        text = self.read(length)[:-1].decode(self.encoding)
        global string_out
        string_out.write(text + "\n")
        return text
    
    def readOP(self):
        res = f"@{self.tell()+4}::"
        #if self.tell() - 4 in flag_list:
        #    res += f"##flag_{flag_list.index(self.tell()-4)}\n"

        op = from_bytes(self.read(1))
        try:
            func = OPList[op][2]
            name = OPList[op][1]
        except:
            print(f"op : {op} not found")
            print(self.tell())
            exit()
        res += name + " " + func(self, "d", None) + "\n"
        return res

class HCB_Decompiler():
    def __init__(self, path, encoding = "932"):
        data = open_file_b(path)
        self.codelen = from_bytes(data[:4])
        self.data = HCB_Reader(data[4:self.codelen])
        self.other = HCB_Reader(data[self.codelen:-2])
        self.encoding = encoding
        self.data.set_encoding(encoding)
        self.other.set_encoding(encoding)

    def read_info(self):
        res = "####INFO####\n"
        res += f"ENTRYPOINT = {self.other.readU32()}\n"
        res += f"BIN = {self.other.read(6).hex()}\n"
        res += f"TITLE = {self.other.readString()}\n"
        res += f"NUM_IMPORTS = {self.other.readU16()}\n"
        idx = 0
        while self.other.tell() < len(self.other.getbuffer()):
            print(self.other.tell(), end="\r")
            type = self.other.readU8()
            func = self.other.readString()
            res += f"{idx}|{func}|{type}\n"
            idx += 1
        return res

    def decompile(self, outpath):
        #self.read_info()
        #while self.data.tell() < len(self.data.getbuffer()):
        #    print(self.data.tell(), end="\r")
        #    self.data.readOP()
        self.data.seek(0)
        self.other.seek(0)

        with open(outpath, "w", encoding = self.encoding) as f:
            while self.data.tell() < len(self.data.getbuffer()):
                f.write(self.data.readOP())
            f.write(self.read_info())

class HCB_Compiler():
    def __init__(self, path) -> None:
        data = open(path, "r", encoding="932").readlines()
        print("Reading file...")
        self.command_list = []
        for i in range(len(data)):
            #print(i, end="\r")
            if data[i] == "####INFO####\n":
                break
            offset, command = data[i].split("::")
            offset = offset[1:]
            command = command[:-1].split(" ", 1)
            if len(command) == 1:
                command.append("")
            self.command_list.append((offset, command))
        i += 1
        self.entrypoint = int(data[i].split(" = ")[1][:-1])
        self.bin = int(data[i+1].split(" = ")[1][:-1], 16).to_bytes(6, "big")
        self.title = data[i+2].split(" = ")[1][:-1]
        self.num_imports = int(data[i+3].split(" = ")[1][:-1])
        i += 4
        self.imports = []
        while i < len(data) and data[i] != "" and data[i] != "\n":
            idx, func, type = data[i].split("|")
            self.imports.append((type[:-1], func))
            i += 1

    def gen_offset_dict(self):
        print("Generating offset dict...")
        self.offset_dict = {}
        length = 4
        for offset, command in self.command_list:
            self.offset_dict[int(offset)] = length
            opname, arg = command
            opcode, func = opdict_funcname[opname]
            length += 1 + func(arg, "l", None)
    
    def compile(self, outpath):
        print("Compiling...")
        self.gen_offset_dict()
        out = []
        for offset, command in self.command_list:
            #print(len(out), end="\r")
            opname, arg = command
            opcode, func = opdict_funcname[opname]
            try:
                out.append(to_bytes(opcode, 1) + func(arg, "c", self.offset_dict))
            except:
                print(f"Error at {offset}")
                print(f"opname : {opname}")
                print(f"arg : {arg}")
                exit()
        out = b"".join(out)
        length = to_bytes(len(out) + 4, 4)
        infos = b""
        infos += to_bytes(self.offset_dict[self.entrypoint], 4)
        infos += self.bin
        infos += to_bytes(len(self.title.encode("932")) + 1, 1) + self.title.encode("932") + b"\x00"
        infos += to_bytes(self.num_imports, 2)
        for type, func in self.imports:
            infos += to_bytes(int(type), 1) + to_bytes(len(func.encode("932")) + 1, 1) + func.encode("932") + b"\x00"
        out = length + out + infos + b"\x00\x00"
        save_file_b(outpath, out)

if __name__ == "__main__":
    hcb = "AstralAirFinale"
    encoding = "932"
    mode = "c"
    if mode == "d":
        init = open(f"{hcb}_string.txt", "w", encoding=encoding)
        init.close()
        string_out = open(f"{hcb}_string.txt", "a", encoding=encoding)
        HCB_Decompiler(f"{hcb}.hcb", encoding=encoding).decompile(f"{hcb}.txt")
    if mode == "c":
        HCB_Compiler(f"{hcb}.txt").compile(f"{hcb}.bch")