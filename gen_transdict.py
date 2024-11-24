from Lib import *

charas = ["科罗娜", "雪雪", "铃音", "落叶", "琴里","日向","幸","叶月","一夏", "name"]
transdict = {}
for chara in charas:
    orifile = open("texts/"+chara+"_ori.txt", "r", encoding="932").readlines()
    transfile = open("texts/"+chara+"_chs.txt", "r", encoding="936").readlines()
    if len(orifile) != len(transfile):
        print("Error: "+chara)
        print("行数不一致")
        exit()
    for i in range(len(orifile)):
        if re.match("[a-zA-Z_]", orifile[i]):
            continue
        if orifile[i] == "\n":
            continue
        if orifile[i].encode("932") == transfile[i].encode("936"):
            continue
        transdict[orifile[i][:-1]] = transfile[i][:-1]
save_json("transdict.json", transdict)
