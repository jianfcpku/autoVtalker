# 一个没什么用的基于示读的半自动VOCALOID中文语调教小程序

写着玩的，没什么用。

本程序读入一段人声朗读的wav文件，及其对应的用praat切分，标记了单字拼音的TextGrid文件，产生一个vsqx文件。

基本原理是利用pyworld提取基频，经过简单的变换和平滑转化为pit参数输出。

TextGrid文件应具有如下格式，空白/噪声区域应为空白标记（当然写成Asp/Sil也行）：

```
File type = "ooTextFile"
Object class = "TextGrid"

xmin = 0 
xmax = 7.407594524119951 
tiers? <exists> 
size = 1 
item []: 
    item [1]:
        class = "IntervalTier" 
        name = "content" 
        xmin = 0 
        xmax = 7.407594524119951 
        intervals: size = 13 
        intervals [1]:
            xmin = 0 
            xmax = 0.16577848741942652 
            text = "" 
        intervals [2]:
            xmin = 0.16577848741942652 
            xmax = 0.5915931364027138 
            text = "ye" 
        (...)
        intervals [13]:
            xmin = 6.239803374506519 
            xmax = 7.407594524119951 
            text = "qing" 
```

要运行此程序，建议在python 3.6以上环境下，同时须有numpy、pyworld、soundfile三个依赖库，按如下命令运行。

```
python autoVtalker.py in.wav in.TextGrid out.vsqx
```

因为我懒得找拼音到XSAMPA的字典，所以输出的vsqx中只有拼音，而没有XSAMPA（都是默认的a），需用VOCALOID打开后全选所有音符，点击插入歌词，然后直接确定，使用VOCALOID内置的字典自动刷新XSAMPA标注。

默认的声库是Yuezhengling V3，可在使用VOCALOID打开后修改，其余参数同理。

如果效果不好，可以调一调平滑窗口大小什么的，当然最重要的还是生成好后自己处理一遍PIT和DYN的细节，所以说这个玩意并没有什么用，可能做好切分的话可以解决一下节奏问题。

样例的语音文件来自标贝中文标准女声音库（https://www.data-baker.com/open_source.html）中的003796.wav。