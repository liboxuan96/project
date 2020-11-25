import os
from xml.etree import ElementTree  # 导入ElementTree模块


def prettyXml(element, indent, newline, level=0):  # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
    if element:  # 判断element是否有子元素
        if element.text == None or element.text.isspace():  # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
            # else:  # 此处两行如果把注释去掉，Element的text也会另起一行
        # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element)  # 将elemnt转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1):  # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        prettyXml(subelement, indent, newline, level=level + 1)  # 对子元素进行递归操作


path = 'C:/Users/PC/Desktop/Annotations' # xml文件存放路径

files=os.listdir(path)
for xmlFile in files:
    tree = ElementTree.parse(os.path.join(path, xmlFile))  # 解析test.xml这个文件，该文件内容如上文
    root = tree.getroot()  # 得到根元素，Element类
    prettyXml(root, '\t', '\n')  # 执行美化方法
    tree.write(os.path.join(path, xmlFile), encoding='UTF-8')
    ElementTree.dump(root)  # 显示出美化后的XML内容