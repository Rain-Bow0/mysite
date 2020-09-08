import xlrd
from openpyxl import Workbook

url = r'C:\Users\Rain_Bow\Documents\Tencent Files\1484261541\FileRecv\党员志愿者信息.xlsx'
url2 = r'C:\Users\Rain_Bow\Documents\Tencent Files\1484261541\FileRecv\123.xlsx'
f = xlrd.open_workbook(url)


name = [
    '张宗榜',
    '王永福',
    '张雨',
    '石晓楠',
    '傅茂松',
    '林睿',
    '钟璐英',
    '周鑫煌',
    '沈溢煌',
    '余琳玲',
    '李镇平',
    '陈启昌',
    '张凯',
    '林华伟',
    '林铮威',
    '杨蓁旎',
    '戴妍',
    '郑千玲',
    '邓健程',
    '颜荣镇',
    '林逸群',
    '陈超颖',
    '王瑞卿',
    '苏凯婷',
    '林立',
    '梅恒权',
    '邱炜旭',
    '郑雅芳',
    '陈心怡',
    '阮君曦',
    '吴雅虹',
    '朱晓倩',
    '王镇隆',
    '林涛',
    '王耀鑫',
    '林晓锋',
    '侯雅倩',
    '林少惠',
    '黄彬煌',
    '许煌标',
    '陈梦雪',
    '刘诗琳',
    '陈苏苏',
    '潘海东',
    '陈友昆',
    '陈明磊',
    '孙承恺',
    '陈智平',
    '胡雅伶',
    '刘朋宇',
]
table = f.sheets()[0]
nrows = table.nrows


wb = Workbook()
# 获取当前活跃的sheet，默认是第一个sheet
ws = wb.active
tt = 1
for i in range(2, nrows):
    if table.cell_value(i, 1) in name:
        ws.append(table.row_values(i))

wb.save(url2)
