"""把文件名里的空格换成下划线。

只用到最基础的语法：import / input / for / if / 字符串方法 / os 模块的两个函数。

用法：
    python batch_rename.py
    然后按提示输入文件夹路径。

默认只打印预览，不会真的改名。
想真正执行，把文件末尾的 APPLY = False 改成 True，再运行一次。
"""

import os

# 1. 问用户要文件夹路径
folder = input("请输入文件夹路径：")

# 2. 列出这个文件夹里所有东西的名字（只是名字，不含路径）
names = os.listdir(folder)

# 3. 一个一个检查
for name in names:
    # 3.1 拼出完整路径，比如  C:\照片\我的 图.jpg
    old_path = os.path.join(folder, name)

    # 3.2 跳过子文件夹，只处理文件
    if not os.path.isfile(old_path):
        continue

    # 3.3 把名字里的空格换成下划线
    new_name = name.replace(" ", "_")

    # 3.4 改完之后和原来不一样，就打印出来
    if new_name != name:
        print(name, "  ->  ", new_name)

print("以上是预览。确认没问题后，把文件里 APPLY = False 改成 True 再运行。")

APPLY = False

# 5. 真正改名（默认不执行）
if APPLY:
    for name in names:
        old_path = os.path.join(folder, name)

        if not os.path.isfile(old_path):
            continue

        new_name = name.replace(" ", "_")

        if new_name != name:
            new_path = os.path.join(folder, new_name)
            os.rename(old_path, new_path)

    print("改名完成。")
