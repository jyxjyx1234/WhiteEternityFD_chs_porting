from Lib import *
from HanziReplacer import *
from HCB_tool import *

new = "AstralAirFinaleHD.txt"
new_trans = "AstralAirFinale_new_trans.txt"
new_file = open(new, "r", encoding="932").read().split("\n")
new_trans_file = open("AstralAirFinale_new_trans.txt", "w", encoding="932")
transdict = open_json("transdict.json")
h = HanziReplacer()
h.ReadTransAndGetHanzidict([transdict])
h.ChangeFont("wenquanyi.ttf", "snow_fd.ttf", "snow_fd")

for i in range(len(new_file)):
    if re.match(r"@.*pushstring [^a-zA-Z_].*", new_file[i]):
        text = re.match(r"@.*pushstring (.*)", new_file[i]).group(1)
        if text in transdict:
            trans = transdict.get(text, text)
            trans = h.hanzitihuan(trans)
        else:
            print(text)
            trans = text
        transtext = re.sub(r"(@.*pushstring )(.*)", lambda x: x.group(1) + trans, new_file[i])
    else:
        transtext = new_file[i]
    new_trans_file.write(transtext + "\n")
new_trans_file.close()
#pack
HCB_Compiler(new_trans).compile(os.path.join("release", new_trans.replace(".txt", ".bch")))
