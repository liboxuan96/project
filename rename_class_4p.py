import os
import os.path
import xml.dom.minidom


# 解析txt文件中的信息：图像编号（6位），字典（5,6,7），id（23,24,25），x1，y1，x2，y2，x3，y3，x4，y4
# 修改class（marker => 5_23, 7_24...）
# 在bndbox中插入x y信息（有序）

def rename_name_x_y() :
    path = "C:\\Users\\PC\\Desktop\\Annotations"

    with open("C:/Users/PC/Desktop/corners.txt") as f:
        for line in f:
            num = line.split()
            # print(num[0],num[6])

            filename = str(num[0]) + ".XML"
            file = os.path.join(path, filename)
            if not os.path.exists(file):
                continue
            dom = xml.dom.minidom.parse(file)   # 打开xml文件
            root = dom.documentElement  # 得到文档元素对象

            '''
            # 提取size信息
            width = root.getElementsByTagName('width')
            height = root.getElementsByTagName('height')
            w = width[0].firstChild.data
            h = height[0].firstChild.data
            # print(w,h)
            '''

            # 提取object信息
            object = root.getElementsByTagName('object')

            # 遍历image中所有marker
            for mark in object:

                bndbox = mark.getElementsByTagName('bndbox')
                # print(len(bndbox))

                x_min = mark.getElementsByTagName('xmin')
                y_min = mark.getElementsByTagName('ymin')
                x_max = mark.getElementsByTagName('xmax')
                y_max = mark.getElementsByTagName('ymax')

                xmin = x_min[0].firstChild.data
                ymin = y_min[0].firstChild.data
                xmax = x_max[0].firstChild.data
                ymax = y_max[0].firstChild.data

                # 判断中心点
                xcenter = (int(num[3]) + int(num[5]) + int(num[7]) + int(num[9])) / 4
                ycenter = (int(num[4]) + int(num[6]) + int(num[8]) + int(num[10])) / 4

                if xcenter > int(xmin) and xcenter < int(xmax) and ycenter > int(ymin) and ycenter < int(ymax):

                    # 修改name
                    name = mark.getElementsByTagName('name')
                    name[0].firstChild.data = num[1] + '_' + num[2]

                    # 修改xmin，ymin，xmax，ymax
                    x_min[0].firstChild.data = str(min(min(int(num[3]), int(num[5])), min(int(num[7]), int(num[9]))))
                    y_min[0].firstChild.data = str(min(min(int(num[4]), int(num[6])), min(int(num[8]), int(num[10]))))
                    x_max[0].firstChild.data = str(max(max(int(num[3]), int(num[5])), max(int(num[7]), int(num[9]))))
                    y_max[0].firstChild.data = str(max(max(int(num[4]), int(num[6])), max(int(num[8]), int(num[10]))))

                    # xi，yi按目标回归点排序 ①左上 ②右上 ③右下 ④左下
                    xmin = int(x_min[0].firstChild.data)
                    ymin = int(y_min[0].firstChild.data)
                    xmax = int(x_max[0].firstChild.data)
                    ymax = int(y_max[0].firstChild.data)

                    # 轮转角点，若有符合条件的就跳出轮转
                    i = 0
                    while i < 4 :
                        if (int(num[3]) == xmin and int(num[4]) < (ymin + ymax) / 2) or (int(num[4]) == ymin and int(num[3]) < (xmin + xmax) / 2) : break
                        num[3], num[4], num[5], num[6], num[7], num[8], num[9], num[10] = num[5], num[6], num[7], num[8], num[9], num[10], num[3], num[4]
                        i = i + 1

                    # 若四个角点都不符合条件，则取xmin所在的角点为第一个角点
                    if i == 4 :
                        while int(num[3]) != xmin :
                            num[3], num[4], num[5], num[6], num[7], num[8], num[9], num[10] = num[5], num[6], num[7], num[8], num[9], num[10], num[3], num[4]

                    # bndbox增加xi，yi节点
                    for i in range(1, 5) :
                        node_name = 'x' + str(i)
                        x = dom.createElement(node_name)
                        value = dom.createTextNode(str(num[2 * i + 1]))
                        x.appendChild(value)
                        bndbox[0].appendChild(x)

                        node_name = 'y' + str(i)
                        y = dom.createElement(node_name)
                        value = dom.createTextNode(str(num[2 * i + 2]))
                        y.appendChild(value)
                        bndbox[0].appendChild(y)

                    print('修改成功', name[0].firstChild.data)

                    # 写入xml文件
                    with open(file, 'w') as fh:
                        dom.writexml(fh)
                        print('写入name/pose OK!')

    f.close()


# 删除ArUco无法识别的标记

def delete_marker() :
    path = "C:\\Users\\PC\\Desktop\\Annotations"

    with open("C:/Users/PC/Desktop/corners.txt") as f:
        for line in f:
            num = line.split()
            # print(num[0],num[6])

            filename = str(num[0]) + ".XML"
            file = os.path.join(path, filename)
            if not os.path.exists(file):
                continue
            dom = xml.dom.minidom.parse(file)  # 打开xml文件
            root = dom.documentElement  # 得到文档元素对象

            # 提取object信息
            object = root.getElementsByTagName('object')

            # 遍历image中所有marker
            for mark in object:
                name = mark.getElementsByTagName('name')
                x1 = mark.getElementsByTagName('x1')
                if len(x1) == 0 or name[0].firstChild.data == 'marker' :
                    # 删除节点
                    print('there is')
                    mark.parentNode.removeChild(mark)

                    # 写入xml文件
                    with open(file, 'w') as fh:
                        dom.writexml(fh)
                        print('写入name/pose OK!')


# 检测有没有不存在任何类别的无效xml文件

def detect_any_marker() :
    path = "C:\\Users\\PC\\Desktop\\Annotations"

    with open("C:/Users/PC/Desktop/corners.txt") as f:
        for line in f:
            num = line.split()
            # print(num[0],num[6])

            filename = str(num[0]) + ".XML"
            file = os.path.join(path, filename)
            if not os.path.exists(file):
                continue
            dom = xml.dom.minidom.parse(file)  # 打开xml文件
            root = dom.documentElement  # 得到文档元素对象

            # 提取object信息
            object = root.getElementsByTagName('object')

            # 检测是否有marker
            if len(object) == 0 :
                print(str(num[0]))


# rename_name_x_y()
# delete_marker()
detect_any_marker()