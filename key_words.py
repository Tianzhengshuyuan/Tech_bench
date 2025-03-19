import json

# 假设 JSON 文件名为 questions.json
with open("conprehensive_questions.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# 初始化分类字典
physics_questions = []
chemistry_questions = []
biology_questions = []
unknown_questions = []

# 关键字列表，用于分类
physics_keywords = ["物理", "正电", "负电", "核反应方程", "电场", "动能", "做功", "内能", "压强", "元电荷", "点电荷", "金属板", "平行板电容器", "电阻", "电容", "电压", "电流", "电势", "动能", "弹簧", "冲量", "库仑力", "折射", "入射", "出射", "波长", "焦距", "摩擦", "重力", "拉力", "磁场", "动量", "轨迹", "匀速", "匀加速", "加速度", "初速度", "水平方向", "空气阻力", "自由落体", "匀速圆周", "简谐", "第一宇宙速度", "理想气体", "砝码", "轨道半径", "并联", "串联"]
chemistry_keywords = ["化学", "燃烧热", "主族", "反应", "化合物", "氧化", "还原", "催化", "煅烧", "阿伏伽德罗常数", "元素周期表", "丁达尔效应", "沉淀", "质量分数", "极性分子", "甲基", "乙基", "硝酸", "硫酸", "盐酸", "醋酸", "碳酸", "酸性", "碱性", "苏打", "重水", "白磷",  "锰", "溴", "苯", "氢气", "氦气", "氟气", "石灰","石英", "同分异构体", "物质的量", "同位素", "离子方程式", "NaOH", "HCl", "mol/L", "pH", "阳离子", "阴离子", "蒸馏", "强酸", "强碱"]
biology_keywords = ["生物", "生命活动", "叶绿素", "叶绿体", "光合作用", "细胞", "酶", "受精卵", "DNA", "RNA", "核酸", "萌发", "氨基酸", "基因", "生态", "萌发", "遗传", "植物", "动物", "生长", "进化", "新陈代谢",  "繁殖", "生殖", "自交", "杂交", "反射弧", "污染", "激素", "酶", "大脑", "甲状腺", "捕食", "过敏", "血管", "蛋白", "淋巴", "有氧呼吸", "无氧呼吸", "食物链", "种群", "免疫", "抗原", "抗体", "线粒体", "细菌", "真菌", "性状", "亲本"]

# 分类函数
def classify(text):
    # 根据关键词判断题目类别
    if any(keyword in text for keyword in physics_keywords):
        return "physics"
    elif any(keyword in text for keyword in chemistry_keywords):
        return "chemistry"
    elif any(keyword in text for keyword in biology_keywords):
        return "biology"
    else:
        return "unknown"

# 遍历数据并分类
for item in data:

    category = classify(item["question"])
    if category == "unknown":
        category = classify(item["A"])
    if category == "unknown":
        category = classify(item["B"])
    if category == "unknown":
        category = classify(item["C"])
    if category == "unknown":
        category = classify(item["D"])

    if category == "physics":
        physics_questions.append(item)
    elif category == "chemistry":
        chemistry_questions.append(item)
    elif category == "biology":
        biology_questions.append(item)
    else:   
        unknown_questions.append(item)

# 将分类结果保存到文件
with open("physics_questions.json", "w", encoding="utf-8") as file:
    json.dump(physics_questions, file, ensure_ascii=False, indent=4)

with open("chemistry_questions.json", "w", encoding="utf-8") as file:
    json.dump(chemistry_questions, file, ensure_ascii=False, indent=4)

with open("biology_questions.json", "w", encoding="utf-8") as file:
    json.dump(biology_questions, file, ensure_ascii=False, indent=4)
    
with open("unknown_questions.json", "w", encoding="utf-8") as file:
    json.dump(unknown_questions, file, ensure_ascii=False, indent=4)

print("分类完成！")