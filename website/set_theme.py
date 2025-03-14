import os
import re
import sys

# gray, red, yellow, green not allowed
color_list = [
    ("fuchsia", "\033[95m"), ("violet", "\033[35m"),
    ("pink", "\033[95m"), ("rose", "\033[35m"),
    ("orange", "\033[91m"), ("amber", "\033[93m"),("emerald", "\033[92m"),
    ("lime", "\033[32m"), ("teal", "\033[36m"),
    ("blue", "\033[94m"), ("sky", "\033[96m"), ("cyan", "\033[36m"),
    ("slate", "\033[37m"), ("stone", "\033[90m")
]
reset_color = "\033[0m"

# 获取脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, "src")
vue_dir = os.path.join(script_dir, "src", "components")

# 颜色与暗黑模式的配置位置
main_page = "App.vue"

# 读取当前的颜色主题
def get_color_theme():
    with open(os.path.join(src_dir, main_page), 'r', encoding='utf-8') as file:
        content_list = file.read().split('\n')
    for line in content_list:
        if "colorTheme" in line:
            color_theme = line.split(': "')[1].replace('"', '').replace(",", "").strip()
            return color_theme
    return None

# 写入颜色主题
def write_color_theme(color_old, color_new):
    with open(os.path.join(src_dir, main_page), 'r', encoding='utf-8') as file:
        content = file.read()
    content = content.replace(f'colorTheme: "{color_old}",', f'colorTheme: "{color_new}",')
    with open(os.path.join(src_dir, main_page), 'w', encoding='utf-8') as file:
        file.write(content)

# 是否为暗黑模式
def get_darkmod():
    with open(os.path.join(src_dir, main_page), 'r', encoding='utf-8') as file:
        content_list = file.read().split('\n')
    for line in content_list:
        if "darkmod" in line:
            isDarkmod = line.split(': ')[1].strip()
            if isDarkmod == "true":
                return True
            else:
                return False
    print("Could not detect color theme.")
    sys.exit(1)

# 写入当前颜色模式
def write_darkmod(old_mod, new_mod):
    with open(os.path.join(src_dir, main_page), 'r', encoding='utf-8') as file:
        content_list = file.read().split('\n')
    for i in range(len(content_list)):
        if "darkmod" in content_list[i]:
            content_list[i] = content_list[i].replace(old_mod, new_mod) 
    with open(os.path.join(src_dir, main_page), 'w', encoding='utf-8') as file:
        file.write("\n".join(content_list))

# 设置新颜色
def set_color(color_old, color_new):
    write_color_theme(color_old, color_new)
    for vue_file in os.listdir(vue_dir):
        file_path = os.path.join(vue_dir, vue_file)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        # 使用正则替换颜色
        content = re.sub(rf'-{color_old}-(\d+)', rf'-{color_new}-\1', content)
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    print(f"Color theme updated to '{color_new}'.")

# 切换 dark/light mod
def set_darkmod(old_mod, new_mod, color_now):
    # 写入新的mod
    write_darkmod(old_mod, new_mod)
    for vue_file in os.listdir(vue_dir):
        file_path = os.path.join(vue_dir, vue_file)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 替换颜色深浅（1000-xxx）
        def replace_color(match):
            color_num = int(match.group(1))
            color_num_new = 1000 - color_num
            return f'-{color_now}-{color_num_new}'

        # 使用正则表达式替换颜色数值
        content = re.sub(rf'-{color_now}-(\d+)', replace_color, content)

        # 替换黑白色
        if new_mod == "true":
            content = content.replace("bg-black", "bg-white")
        else:
            content = content.replace("bg-white", "bg-black")
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    print(f"Switch to darkmod: {new_mod}")

# 设置颜色主函数
def update_color_theme():
    # 获取当前颜色主题
    color_old = get_color_theme()
    if color_old:
        print("Color Theme Now: %s" % color_old)
    else:
        print("Can not get theme now.")
        os._exit(1)

    print("Available Colors:")
    for color, ansi_code in color_list:
        print(f"{ansi_code}{color}{reset_color}", end=" ")
    print()

    choice = input("Your choice: ").strip()

    # 检查选择是否在可用颜色中
    available_colors = [color for color, ansi in color_list]
    if choice not in available_colors:
        print(f"'{choice}' is not in the available list.")
    elif choice == color_old:
        print("The selected color is already the current theme.")
    else:
        set_color(color_old, choice)

# 设置暗黑模式主函数
def update_darkmod():
    # 获取当前darkmod状态
    old_mod = get_darkmod()
    print("Darkmod now: %s" % old_mod)
    if old_mod:
        old_mod = "true"
        new_mod = "false"
    else:
        old_mod = "false"
        new_mod = "true"
    # 读取当前颜色设置
    color_now = get_color_theme()
    if not color_now:
        print("Can not get theme now.")
        os._exit(1)
    # 切换模式
    set_darkmod(old_mod, new_mod, color_now)

def help():
    print("Usage: python set_theme.py -c/-d")
    os._exit(1)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        help()
    if sys.argv[1] == "-c":
        update_color_theme()
    elif sys.argv[1] == "-d":
        update_darkmod()
    else:
        help()