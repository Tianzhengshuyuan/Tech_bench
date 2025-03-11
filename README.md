使用脚本将文件夹中的.doc批量转换为.docx，第一个参数是源文件夹，第二个是目标文件夹
```bash
./doc_to_docx.sh /root/test /root/test_docx 
```

预处理word文档，删除smartTag，只保留里面的<w:r>
```bash
python remove_smartTag.py  --docx_name=2004年云南高考理科综合真题及答案
```

打开图片公式识别的话，程序运行较慢，使用下面命令关闭
```bash
 python docx_to_json.py  --docx_name=2001年陕西高考理综真题及答案 --latex=off > log.txt
``` 

直接使用.sh脚本
```bash
./run.sh 2004年云南高考理科综合真题及答案 off > log.txt
```

待解决的问题：
1. 删除目录里的A3 word版
2. 删除原卷和无答案的word文档
3. 处理答案形式：
![答案1](./images/答案1.png)
以及前半部分是原卷，后半部分如图的情况
4. 处理答案形式：
![答案2](./images/答案2.png)
5. 处理答案形式：
![答案3](./images/答案3.png)
以及前半部分是原卷，后半部分如图的情况
6. 处理答案形式：
![答案4](./images/答案4.png)
7. 前半部分是原卷、后半部分是答案的情况，如何防止重复？
8. 如何区分选择题和非选择题
9. 如何在理综试卷中区分物理、化学、生物
10. 如何处理有图的情况





无法解决的问题：
1. Simpletex无法正确识别λ，尝试裁剪图片只保留公式部分，但并没有用
![word文档内容](./images/lamda.png)
会被识别为
![识别结果](./images/wrong_lamda.png)

