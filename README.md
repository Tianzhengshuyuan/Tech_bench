使用.sh脚本：
```bash
./run.sh 2004年云南高考理科综合真题及答案 off > log.txt

预处理word文档，删除smartTag，只保留里面的<w:r>
```bash
python remove_smartTag.py  --docx_name=2004年云南高考理科综合真题及答案

打开图片公式识别的话，程序运行较慢，使用下面命令关闭：
```bash
 python docx_to_json.py  --docx_name=2001年陕西高考理综真题及答案 --latex=off > log.txt