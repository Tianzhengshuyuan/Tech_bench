# 使用方法
使用脚本将文件夹中的.doc批量转换为.docx，第一个参数是源文件夹，第二个是目标文件夹
```bash
./doc_to_docx.sh /root/test /root/test_docx 
```
在linux中使用soffice把doc转为docx会丢失wmf形式的公式，改为在windows中使用word文档的vba自动将.doc转为.docx：
1. Alt+F11打开vba
2. 复制代码如下，进行批量处理
```vba
Sub BatchDocToDocxRecursiveWithDocxCopy()
    Dim inputFolderPath As String
    Dim outputFolderPath As String
    Dim logFilePath As String

    ' 选择包含 .doc 文件的输入文件夹
    With Application.FileDialog(msoFileDialogFolderPicker)
        .Title = "选择包含 DOC 文件的文件夹"
        If .Show = -1 Then
            inputFolderPath = .SelectedItems(1) & "\"
        Else
            Exit Sub
        End If
    End With

    ' 选择保存转换后文件的输出文件夹
    With Application.FileDialog(msoFileDialogFolderPicker)
        .Title = "选择保存 DOCX 文件的文件夹"
        If .Show = -1 Then
            outputFolderPath = .SelectedItems(1) & "\"
        Else
            Exit Sub
        End If
    End With

    ' 日志文件路径
    logFilePath = outputFolderPath & "ErrorLog.txt"

    ' 调用递归函数处理文件夹
    ProcessFolderWithDocxCopy inputFolderPath, outputFolderPath, logFilePath

    MsgBox "批量处理完成！", vbInformation
End Sub

Sub ProcessFolderWithDocxCopy(ByVal inputFolder As String, ByVal outputFolder As String, ByVal logFile As String)
    Dim fileName As String
    Dim doc As Document
    Dim fso As Object
    Dim folderItem As Object
    Dim logText As String

    ' 创建输出文件夹（如果不存在）
    If Dir(outputFolder, vbDirectory) = "" Then
        MkDir outputFolder
    End If

    ' 遍历当前文件夹中的所有文件
    fileName = Dir(inputFolder & "*.*")
    Do While fileName <> ""
        On Error Resume Next ' 开始错误捕捉
        If InStr(fileName, ".docx") > 0 Then
            ' 如果是 .docx 文件，直接复制到输出文件夹
            FileCopy inputFolder & fileName, outputFolder & fileName
            If Err.Number <> 0 Then
                ' 如果复制失败，记录到日志
                logText = "复制失败: " & inputFolder & fileName & " 错误代码: " & Err.Number & " 描述: " & Err.Description & vbCrLf
                AppendToLog logFile, logText
                Err.Clear
            End If
        ElseIf InStr(fileName, ".doc") > 0 Then
            ' 如果是 .doc 文件，打开并转换为 .docx
            Set doc = Documents.Open(inputFolder & fileName)
            If Err.Number <> 0 Then
                ' 如果打开失败，记录到日志
                logText = "打开失败: " & inputFolder & fileName & " 错误代码: " & Err.Number & " 描述: " & Err.Description & vbCrLf
                AppendToLog logFile, logText
                Err.Clear
            Else
                doc.SaveAs2 outputFolder & Replace(fileName, ".doc", ".docx"), wdFormatXMLDocument
                If Err.Number <> 0 Then
                    ' 如果保存失败，记录到日志
                    logText = "保存失败: " & inputFolder & fileName & " 错误代码: " & Err.Number & " 描述: " & Err.Description & vbCrLf
                    AppendToLog logFile, logText
                    Err.Clear
                End If
                doc.Close
            End If
        End If
        On Error GoTo 0 ' 关闭错误捕捉
        fileName = Dir
    Loop

    ' 遍历子文件夹
    Set fso = CreateObject("Scripting.FileSystemObject")
    For Each folderItem In fso.GetFolder(inputFolder).SubFolders
        ' 递归调用子文件夹
        ProcessFolderWithDocxCopy folderItem.Path & "\", outputFolder & folderItem.Name & "\", logFile
    Next
End Sub

Sub AppendToLog(ByVal logFile As String, ByVal logText As String)
    Dim logFileNumber As Integer

    ' 打开日志文件（如果不存在则创建）
    logFileNumber = FreeFile
    Open logFile For Append As #logFileNumber
    Print #logFileNumber, logText
    Close #logFileNumber
End Sub
```
下面的文档无法转换（手动另存为也不行，因此放弃）：
2001年上海高考理综真题及答案
2001年天津高考理科真题及答案
2003年河北高考理综真题及答案
2004年浙江高考理科综合真题及答案
2001年上海高考理综真题及答案
2001年天津高考理科真题及答案
2005年江苏高考物理真题及答案
2003年河北高考理综真题及答案
2004年浙江高考理科综合真题及答案
2009年浙江省高考物理（含解析版）
2010年高考福建理综物理试题(含答案)

删除名字中包含“A3”的文件夹、名字中包含“原卷”的文件，物理docx是从windows机器传来的文件夹，包含docx文档
```bash
./preprocess.sh 物理_docx 物理_docx2
```

处理名字中包含特殊字符从而影响解析的问题
```bash
./rename.sh
```

预处理word文档，删除smartTag，只保留里面的<w:r>
```bash
python remove_smartTag.py  --docx_name=2004年云南高考理科综合真题及答案
```

打开图片公式识别的话，程序运行较慢，使用下面命令关闭
```bash
 python docx_to_json.py  --docx_name=2001年陕西高考理综真题及答案 --json_name=2001年陕西高考理综真题及答案 --latex=off > log.txt
``` 

使用.sh脚本，执行一个文件从.docx到.json的转换
```bash
./run_one.sh 2004年云南高考理科综合真题及答案 off > log.txt
```

使用.sh脚本，执行一个文件夹里的所有文件从.docx到.json的转换（开启公式识别将近6小时）
```bash
./run_all.sh GAOKAO off > log.txt
```

区分理综里的物理、化学、生物题
1. 使用k_means方法：
```bash
python extract_Comprehensive_questions.py
python k_means.py
```

2. 使用关键词方法：
```bash
python extract_Comprehensive_questions.py
python key_words.py
``` 

3. 使用逻辑回归分类器——准确率:0.9611764705882353
extract_train_data将output.json去重、提取单一学科的题目用于训练
extract_Comprehensive_questions.py从理化生的output.json中提取需要做区分的题目（理综）
python ml_classifier.py logistic将分类好的题目附加到对应的学科的输出中
```bash
./preprocess.sh ./物理_docx ./物理_docx2
./run_all.sh 物理_docx2 off
mv json/output.json json/output_phy.json
./preprocess.sh ./化学_docx ./化学_docx2
./run_all.sh 化学_docx2 off
mv json/output.json json/output_che.json
./preprocess.sh ./生物_docx ./生物_docx2
./run_all.sh 生物_docx2 off
mv json/output.json json/output_bio.json
python extract_train_data.py
python extract_Comprehensive_questions.py
python ml_classifier.py logistic
```

4. 使用支持向量机——准确率：0.9705882352941176
```bash
python ml_classifier.py svm
```

5. 使用朴素贝叶斯方法——准确率：0.9705882352941176
```bash
python ml_classifier.py naive_bayes
```

6. 使用bert模型——准确率：0.9764705882352941 时间：40分钟
```bash
python bert_classifier.py
```

去除重复的条目，统计ABCD选项、answer的缺失率
```bash
python postprocess.py
```

去除包含“图”关键词的题目
```bash
python exclude_pictures.py --input_file=json/phy_only.json --output_file=json/phy_no_picture.json
```

- 一个完整的工作流程belike:
在windows中完成doc->docx的转换，传到linux
```bash
rsync -av --progress --partial -e "ssh"  /mnt/c/Tech_bench/docx root@192.168.2.65:~/tech_bench/物理_docx
```
```bash
./preprocess.sh ./物理_docx ./物理_docx2
./run_all.sh 物理_docx2 off
python postprocess.py
```

识别可以通过数字扩展的题目
```bash
python find_questions_with_number.py --train_file=json/labeled_questions.json --test_file=json/phy_no_picture.json
```

word2vec环境配置
```bash
conda create -yn word2vec python=3.10
conda activate word2vec
pip install spacy==3.5.0
pip install gensim
python -m spacy download zh_core_web_sm 
python word2vec_paraphrase.py
```

word2vec 预训练模型下载：  
https://github.com/to-shimo/chinese-word2vec  
https://github.com/Embedding/Chinese-Word-Vectors   

使用bert做近义词替换  
环境配置：
```bash
conda create -yn bert python=3.10
conda activate bert
pip install spacy==3.5.0
pip install torch
pip install numpy==1.26.4 
pip install transformers
pip install scikit-learn
python -m spacy download zh_core_web_sm 
pip install datasets 
pip install 'accelerate>=0.26.0' 
pip install jieba
```
wobert或wo_phy还需安装
```bash
pip install git+https://github.com/JunnYu/WoBERT_pytorch.git
```
运行命令：
```bash
python bert_paraphrase.py 
python bert_paraphrase.py --physbert 
python bert_paraphrase.py --fine_tune 
python bert_paraphrase.py --wobert
```
微调bert模型
- cpu 环境  
环境配置(参考[bert4keras | github](https://github.com/bojone/bert4keras?tab=readme-ov-file))：
```bash
conda create -yn bert_train python=3.7
conda activate bert_train
pip install tensorflow==1.14.0
pip install keras==2.3.1
pip install bert4keras
pip install protobuf==3.20.0
pip install jieba
```
训练命令(代码参考 [WoBERT | github](https://github.com/ZhuiyiTechnology/WoBERT)和[Nezha的增量预训练探索(基于bert4keras)](https://zhuanlan.zhihu.com/p/500437589))：
```bash
python bert_train.py
```
得到文件夹wo_phy，包含checkpoint、wo_phy_model.data-00000-of-00001、wo_phy_model.index、wo_phy_model.meta四个文件，复制tech_bench/chinese_wobert_L-12_H-768_A-12中的bert_config.json以及训练得到的new_vocab.txt到wo_phy中，修改bert_config.json中vocab_size大小，然后使用下面命令将tensorflow模型转换为pytorch：  
环境配置：
```bash
conda create -yn tf2pt python=3.10
conda activate tf2pt
pip install tensorflow
pip install torch
pip install transformers==4.30.0
```
```bash
python tf2pt.py
```
上述指令将得到wo_phy_pytorch文件夹，包含pytorch_model.bin，复制bert_config.json和vocab.txt到这个文件夹中，bert_config.json改名config.json，之后可以使用下面命令做同义词替换：  
环境配置：
```bash

```bash
python bert_paraphrase.py --wo_phy
```

- gpu 环境  
环境配置  
ubuntu18.04  
从[这里][(https://developer.nvidia.com/cuda-10.0-download-archive?target_os=Linux&target_arch=x86_64&target_distro=Ubuntu&target_version=1804&target_type=runfilelocal)下载cuda 10.0，   
从[这里](https://developer.nvidia.com/rdp/cudnn-archive)下载cuDNN v7.4.1(Nov 8, 2018), for CUDA 10.0，包括三部分：  
1. cuDNN Runtime Library for Ubuntu18.04 (Deb)
2. cuDNN Developer Library for Ubuntu18.04 (Deb)
3. cuDNN Code Samples and User Guide for Ubuntu18.04 (Deb)  
全部传到目标主机

安装cuda 10.0命令如下，除了xconfig都选yes或默认
```bash
sudo sh cuda_10.0.130_410.48_linux.run
```

在~/.zshrc中添加
```bash
# added by cuda 10.0 installer
export PATH="/usr/local/cuda-10.0/bin:$PATH"
export LD_LIBRARY_PATH="/usr/local/cuda-10.0/lib64:$LD_LIBRARY_PATH"
```
然后
```bash
source ~/.zshrc
```

使用下面命令查看是否安装成功
```bash
nvidia-smi
nvcc -V
cd /usr/local/cuda-10.0/samples/1_Utilities/deviceQuery
sudo make && ./deviceQuery
```

安装 cuDNN 7.4.1 按顺序使用下面命令
```bash
sudo dpkg -i libcudnn7_7.4.1.5-1+cuda10.0_amd64.deb
sudo dpkg -i libcudnn7-dev_7.4.1.5-1+cuda10.0_amd64.deb
sudo dpkg -i libcudnn7-doc_7.4.1.5-1+cuda10.0_amd64.deb
sudo cp /usr/include/cudnn.h /usr/local/cuda/include
sudo chmod a+x /usr/local/cuda/include/cudnn.h
```
使用下面命令检查是否安装成功
```bash
cat /usr/local/cuda/include/cudnn.h | grep CUDNN_MAJOR -A 2
```

最后配置 conda 环境
```bash
conda create -yn bert_train python=3.7
conda activate bert_train
pip install tensorflow-gpu==1.14.0
pip install keras==2.3.1
pip install bert4keras
pip install protobuf==3.20.0
pip install jieba
```

调用大模型的api接口，测试做原题的正确率以及是否能识别同义词替换后的题的逻辑错误
调用deepseek api接口（all_new代表只测试新题）：
```bash
python get_deepseek_answer.py
python get_deepseek_answer.py --all_new 
```
随机选择100题，做同义词替换，然后从原题和该题中随机选题目测试：
下面指令中100代表采样的题目数，all_new代表是否全使用新题，random代表随机选出来100题还是取某文件的前100题
```bash
./right_or_not.sh 100 all_new random
```

调用 gpt api接口
修改openai的连接规则为使用美丽国节点
```yaml
- { name: '🧲 OpenAI', type: select, proxies: [🇺🇸US丨芝加哥, 🇺🇸US丨洛杉矶, 🇬🇧GB丨伦敦, 🇩🇪DE丨法兰克福] }
```
然后开启clash并export
```bash
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
```
```bash
export OPENAI_API_KEY=sk......
python get_openai_answer.py 
```

# 已解决的问题
- 【ok】删除目录里的A3 word版
- 【ok】删除无答案的word文档
- 【ok】前半部分是原卷、后半部分是答案的情况，如何防止重复？
    - 序号重复则跳过
- 【ok】如何区分选择题和非选择题？
    - 删除full_text中“第Ⅱ卷”、“二、”后的所有内容——有的文档里没有这些关键词
    - 删除.json中不完整的条目？
- 【ok】处理答案形式：（2023年高考物理真题（北京自主命题）（解析版））
![答案1](./images/答案1.png)
以及前半部分是原卷，后半部分如图的情况（2020年高考全国I卷物理试题及答案）
- 【ok】处理答案形式：
![答案2](./images/答案2.png)
(2016年高考全国I卷物理试题及答案) (1998年广东高考物理真题及答案)
- 【ok】处理答案形式：
![答案5](./images/答案5.png) 
(2013高考福建卷理综物理部分(含答案))

- 【ok】处理答案形式：
![答案3](./images/答案3.png)
以及前半部分是原卷，后半部分如图的情况
（2008年全国统一高考物理试卷（全国卷ⅰ）（含解析版））
（2015高考安徽物理试卷及答案）
- 【ok】处理答案形式：
![答案4](./images/答案4.png)（2008安徽高考物理试卷及答案）
- 【ok】处理答案形式：
![答案7](./images/答案7.png)（1995年广东高考物理真题及答案）（1995年黑龙江高考物理真题及答案）
- 【ok】处理答案形式：
![答案11](./images/答案11.png)（2003年黑龙江高考理综真题及答案 同 2003年新疆高考理综真题及答案）
![答案6](./images/答案6.png)（2002年陕西高考理科综合真题及答案 同 2002年西藏高考理科综合真题及答案）

- 【ok】如何在理综试卷中区分物理、化学、生物？
    - 人工区分？工作量大
    - 使用关键词区分？
    - 在线大语言模型？尝试了gpt-4o、kimi、deepseek，准确性好，但是无法批量处理，只能返回一小部分结果
    - 本地部署开源大语言模型？
    - 聚类？k-means分类完全不准确
    - 支持向量机、逻辑回归、朴素贝叶斯？https://blog.csdn.net/haha0332/article/details/112575122
    - bert模型

# 待解决的问题
## 答案解析问题
![答案10](./images/答案10.png)（2008年高考贵州理综物理试题(含答案)）
![答案12](./images/答案12.png)（2000年湖南高考物理真题及答案）
![答案13](./images/答案13.png)（2019年全国统一高考物理试卷（新课标ⅰ）（含解析版））（2019年全国统一高考物理试卷（新课标ⅱ））
![答案22](./images/答案22.png)（2009年高考贵州理综物理试题(含答案)）

![答案14](./images/答案14.png)（2016年浙江省高考物理【10月】（含解析版））这里和现有逻辑不匹配是因为现有的re.match从开头开始匹配
（2011年浙江省高考物理（含解析版））
（2017年浙江省高考物理【4月】（含解析版））
![答案15](./images/答案15.png)（2014年上海市高中毕业统一学业考试物理试卷（word解析版））
![答案16](./images/答案16.png)（2006年四川高考理综真题及答案）（2007年宁夏高考理科综合真题及答案）——两种答案形式
![答案18](./images/答案18.png)（2017年浙江省高考物理【11月】（含解析版）——图片形式的答案
（2018年浙江省高考物理【11月】（含解析版））（2016年浙江省高考物理【4月】）
![答案19](./images/答案19.png)（2010年浙江省高考物理（含解析版））（2008年浙江省高考物理（含解析版）
![答案20](./images/答案20.png)（2017年上海市高中毕业统一学业考试物理试卷（答案版））（2003年江苏高考物理真题及答案）
![答案21](./images/答案21.png)（2013年上海市高中毕业统一学业考试物理试卷（word解析版））
![答案23](./images/答案23.png)（2015年上海市高中毕业统一学业考试物理试卷（答案版））
![答案24](./images/答案24.png)（2015年浙江省高考物理【6月】（含解析版））
![答案25](./images/答案25.png)（2012广东高考物理试卷(及答案)）
![答案26](./images/答案26.png)（2012年上海市高中毕业统一学业考试物理试卷（word解析版））（2013广东高考物理试卷(及答案)）
![答案27](./images/答案27.png)（2015年浙江省高考物理【10月】）
![答案28](./images/答案28.png)（2015高考福建卷理综物理部分(含答案)）
![答案29](./images/答案29.png)（2013年高考四川理综物理）
![答案30](./images/答案30.png)（2020年上海市高中毕业统一学业考试物理试卷（word解析版））
![答案31](./images/答案31.png)（2007年上海高考理科综合能力测试真题及答案）

- 没有冒号的“故选”——是否需要处理，加上之后可能影响其他答案识别？
![答案8](./images/答案8.png) （2012高考福建卷理综物理部分(含答案)）
![答案9](./images/答案9.png) （2011年高考贵州理综物理试卷(含答案)）
![答案17](./images/答案17.png) （2011广东高考物理试卷(及答案)）
前一半检查完了/4673

## 选项解析问题
-  例如：“2015高考安徽物理试卷及答案” 解析内容为空
    - 原因是A、B、C、D是表格中的单元格，但是其他文档都不是这样的，放弃处理此文档
检查到613/3180

## 题目解析问题
- 题目中的公式如何识别？
    - wmf形式
    - png形式 （1999年山西高考物理真题及答案）（2018年全国统一高考物理试卷（新课标ⅲ）（含解析版））
- 题目中的表格如何识别？

## word文档中换行符不是段落结束符，影响解析
![换行符](./images/line.png) （1994年新疆高考物理真题及答案）
Alt+F11，插入-模块-粘贴下面的内容-保存-关闭
```vba
Sub ReplaceSoftBreaksWithParagraphs()
    ' 启动查找和替换功能
    With Selection.Find
        .ClearFormatting
        .Replacement.ClearFormatting
        ' 查找软换行符（向下箭头）
        .Text = "^l"
        ' 替换为段落标记（硬换行符）
        .Replacement.Text = "^p"
        .Forward = True
        .Wrap = wdFindContinue
        .Format = False
        .MatchCase = False
        .MatchWholeWord = False
        .MatchWildcards = False
        .MatchSoundsLike = False
        .MatchAllWordForms = False
        ' 执行替换操作
        .Execute Replace:=wdReplaceAll
    End With
End Sub
```
在要转换的文档中按Alt+F8，运行ReplaceSoftBreaksWithParagraphs

## 如何处理有图的情况
-图片无法使用脚本提取，因为是根据位置决定和哪一道题绑定在一起，可能会被绑定到相邻的题目里
-rId和image的对应关系在\word\_rels\document.xml.rels中
1. 题目、图片、选项在三个连续的<w:p>里（2002年陕西高考理科综合真题及答案第3题）
![图片1](./images/图片1.png)
2. 前半部分题目、图片、后半部分题目在三个连续的<w:p>里（2002年陕西高考理科综合真题及答案第14题）
![图片2](./images/图片2.png)
3. 17题的图混在16题里，16题题目是一个段落，17题的图和16提的选项是一个段落
   18题的图混在17题里，17题题目是一个段落，18题的图和17题的选项是一个段落
   19题没有出现“图”关键词，但有图
   20题的图和19题的C在一个段落

## 动态生成问题
可以考虑动态生成的题目：
数字的替换
```bash
    {
        "question": "4.若元素A的半衰期为4天，元素B的半衰期为5天，则相同质量的A和B，经过20天后，剩下的质量　之比m_A:m_B=(　　　)\n　",
        "A": "30:31",
        "B": "31:30",
        "C": "1:2",
        "D": "2:1",
        "index": "4",
        "answer": "C",
        "exam": "1993年重庆高考物理"
    },
    {
        "question": "2．（6分）为了探测引力波，“天琴计划” 预计发射地球卫星P，其轨道半径约为地球半径的16倍；另一地球卫星Q的轨道半径约为地球半径的4倍。P与Q的周期之比约为（　　）\n",
        "A": "2：1",
        "B": "4：1",
        "C": "8：1",
        "D": "16：1",
        "index": "2",
        "answer": "C",
        "exam": "2018年全国统一高考物理试卷（新课标ⅲ）"
    },
```
温度标志着物体内大量[可选]的剧烈程度
```bash
    {
        "question": "3．（6分）下列说法正确的是（　　）\n",
        "A": "温度标志着物体内大量分子热运动的剧烈程度",
        "B": "内能是物体中所有分子热运动所具有的动能的总和",
        "C": "气体压强仅与气体分子的平均动能有关",
        "D": "气体膨胀对外做功且温度降低，分子的平均动能可能不变",
        "index": "3",
        "answer": "A",
        "exam": "2019年北京市高考物理试卷"
    },
```
前面的描述语言可以换成最新的新闻
```bash
    {
        "question": "6．（6分）2019年5月17日，我国成功发射第45颗北斗导航卫星，该卫星属于地球静止轨道卫星（同步卫星）。该卫星（　　）\n",
        "A": "入轨后可以位于北京正上方",
        "B": "入轨后的速度大于第一宇宙速度",
        "C": "发射速度大于第二宇宙速度",
        "D": "若发射到近地圆轨道所需能量较少",
        "index": "6",
        "answer": "D",
        "exam": "2019年北京市高考物理试卷"
    },
```
近义词替换方法：
- word2vec
- bert
- 是否需要一个同义词列表？？
- 只选择top1吗？

word2vec替换效果：
- 正常：柴油->汽油 温度->环境温度 程度->程度较高 动能->能量 折射率->折光率 泥潭->泥沼 卫星->同步卫星 动量->动量定理 微粒->粒子 总和->之和 方程->方程组 波长->光波长 频率->frequency 结合->相结合
- 怪异：过程->N点 运动->N点 说法->幅图 波形->整形电路 加速度->大小为g 重力->大小为g 速度->度a 方向->沿x a->b T->P △t->{a 位置->0时 电势->电偶层 单色->CMY 粒子->质心系 质量->电荷量 大小->安培力 冲量->惯性力 钢珠->焦桃 周期->质量为M 半径->质量为M 振动->简谐 振幅->波腹 地面->A点 地球->球绕 电流->示数 半径为R->质量为M 分子->质子转移 内->银面 电荷数->正下 距离->O点 小->大 物理量->谐振子

bert替换效果:
- 正常：波形->波长 粒子->电子 地面->地球 方程->过程 说法->方法 电势->电场 加速度->加速有 说法->说明 振动->移动 动能->势量 分子->粒子 内->动 
- 怪异：1->2 4->5 合外力->紫力力 小->大 程度->程。 a->b 位置->点。 单色->蓝位 (c->(这 sinθ倍->m的两s 若速度->若曲度 若动->若不 改变量->不变 冲量->动。重力->阻力 钢珠->弹铁 动能->功作 动量->质作 结合->化构 

# 无法解决的问题：
1. Simpletex无法正确识别λ，尝试裁剪图片只保留公式部分，但并没有用
![word文档内容](./images/lamda.png)
会被识别为
![识别结果](./images/wrong_lamda.png)
2. 题号和A.不是文本，而是自动生成的
![word文档内容](./images/auto.png)（2023年高考物理真题（北京自主命题）（解析版））（2015广东高考物理试卷(及答案)）
3. 文件叫解析版实际没有答案（2021年天津市高考物理试卷解析版）（2005年广西高考理科综合真题及答案）
4. 试卷和答案题号不对应（2019年高考全国I卷物理试题及答案）
5. 使用这个下箭头的换行不会被解析为两个段落
![问题1](./images/问题1.png)