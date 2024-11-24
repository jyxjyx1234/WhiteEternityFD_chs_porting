# 星辰恋曲的白色永恒FD HDver——汉化补丁文本移植

本教程仅供交流学习，不提供任何带有xmoe汉化组汉化文本的文件。

写这个文档时，hd版尚未发售，这里假设了hd版的引擎并未作大改动。

20241124

## 需要的工具

python 3.x

## 汉化文本提取

汉化移植首先得提取出原汉化补丁的文本，得到原文和译文的对应表。

众所周知，fvp的文本存储在hcb格式的虚拟机脚本中，有很多现成的工具可以将其解析为可读的虚拟机汇编代码，从而实现修改文本。

然而，xmoe汉化组的汉化补丁中，并没有修改后的hcb文件，而是通过hook了文本读取函数，替换了文本。我虽然在内存中能找到所有的译文，但是水平有限，并没有能将译文和原文相对应。

为此，我写了一个程序，能够在游戏运行时将游戏的文本输出到游戏目录下的output.txt中。源码见byfd_hook文件夹。编译好的dll在byfd_hook_release文件夹中。将byfd_hook_release中所有文件放入带有汉化补丁的**原版**游戏的目录，注意不要有中文路径。

建议的提取步骤：先启动生肉，skip完一条线，退出游戏，将output.exe命名为 角色名_ori.txt（"科罗娜","雪雪","铃音","落叶","琴里","日向","幸","叶月","一夏"）。然后启动汉化版，同样skip完一条线，退出游戏，将output.exe命名为 角色名_chs.txt。每条线分别操作，中间注意不要点开设置界面。同一个角色的ori和tra文件行数应当一致。最后，将所有ori和tra文件复制到texts文件夹。如果不按此步骤，gen_transdict.py中的内容需要自行修改。

此方法人名不能提取，我手动翻译后放到了texts/name_chs.txt以及texts/name_ori.txt中，可以直接使用。

## 建立译文字典

接下来的步骤，如果有一定的编程基础，应该很好实现了，不用继续往下看了。这里我也提供了相应的python脚本可以直接使用。在生成了snow.txt和snow_chs.txt后，运行：

```bat
python gen_transdict.py
```

目录下会生成一个transdict.json，里面有原文和译文的对应。

## HD版HCB文件解析

xmoe汉化组开源了一个hcb脚本的解析工具，白永本体可以直接用，但是白永fd疑似没法用，所以我借鉴了大佬的源码，用python重新搓了个。这里就用我自己搓的工具了。

虽然写这个文档时hd版还没发售，但是应该不会有很大差异。将HD版的AstralAirFinaleHD.hcb（也可能是别的文件名，这里暂且这么称呼，之后的代码中均采用这个名称）放到本工具的目录下，在当前目录下运行：

```bat
python hcb_tool.py d AstralAirFinaleHD.hcb 932
```

运行完毕后，目录下会出现AstralAirFinaleHD.txt和AstralAirFinaleHD_string.txt文件，分别为汇编代码以及所有的文本。AstralAirFinaleHD_string.txt仅为调试用，之后不会用到。

## 导入译文

汉化补丁中，采用了gbk编码进行注入。我技术水平有限，之前制作f社老作的机翻补丁时采用gbk编码注入没成功过，这里就使用了字体替换的方法，通过自己做的一个小工具进行实现。

写这个文档时hd版还没发售，所以代码只是脑测。在生成了AstralAirFinaleHD.txt和transdict.json后运行：

```bat
python injecct_trans.py
```

在release目录下生成了AstralAirFinaleHD.bch文件。适当的重命名，与hd版的hcb文件同名。

由于hd版可能更改了文本，所以可能有部分没有匹配到译文的文本。这部分文本会打印出来，需要自行手动修正。（但是那些地名请勿修正，否则可能会有bug。）

## 补丁

补丁所需的文件在release文件夹中。可能需要更改hook.ini中的第二行的游戏原exe名。覆盖到游戏目录即可，无需再转区，无需安装字体，不支持中文目录。
