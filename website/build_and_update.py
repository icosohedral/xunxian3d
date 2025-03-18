import os
import shutil, subprocess
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def rewrite_api(env):
    API_FILE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "src", "api.js")
    test_url = 'http://localhost:18000'  # 本地测试环境URL
    prod_url = '/'  # 生产环境URL
    if env == "test":
        url = test_url
    else:
        url = prod_url
    with open(API_FILE_PATH, "r", encoding='utf8') as file:
        content = file.read()
    content_list = content.split('\n')
    lines = []
    for line in content_list:
        if 'baseURL' in line:
            line = "baseURL: '%s'," % url
        lines.append(line)
    with open(API_FILE_PATH, "w", encoding='utf8') as file:
        file.write("\n".join(lines))

def print_info(message):
    print(f"{Fore.BLUE}[info]{Style.RESET_ALL} {message}")

def print_success(message):
    print(f"{Fore.GREEN}[succ]{Style.RESET_ALL} {message}")

def print_error(message):
    print(f"{Fore.RED}[error]{Style.RESET_ALL} {message}")

def build():
    print_info("Running build command...")
    # 设置为生产环境URL
    rewrite_api(env="prod")

    res = subprocess.run("npm run build", shell=True, capture_output=True, text=True, encoding="utf-8", errors="ignore")

    print_info("Build command output:\n" + res.stdout)  # 改成 res.stdout
    if "Build complete" not in res.stdout:
        print_error("Build failed.")
        return False
    # 还原 api.js 文件为测试环境 URL
    rewrite_api(env="test")
    print_success("Build successful.")
    return True

def clear_folder(folder):
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)  # 删除文件或符号链接
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # 删除子目录及其内容
            except Exception as e:
                print_error(f'Failed to delete {file_path}. Reason: {e}')
    else:
        print_info(f"The folder {folder} does not exist.")

def move():
    print_info("Starting to move files...")

    script_directory = os.path.dirname(os.path.abspath(__file__))
    backend_folder = os.path.join(os.path.dirname(script_directory), "backend")
    dist_folder = os.path.join(script_directory, 'dist')
    static_folder = os.path.join(backend_folder, 'vercel_app', "static")
    templates_folder = os.path.join(backend_folder, 'vercel_app', "templates")

    print_info(f"Script directory: {script_directory}")
    print_info(f"Backend folder: {backend_folder}")
    print_info(f"Dist folder: {dist_folder}")
    print_info(f"Static folder: {static_folder}")
    print_info(f"Templates folder: {templates_folder}")

    # Delete specific old files in static folder
    try:
        print_info("Deleting old static files (css, js folders, media folder content, and favicon.ico)...")
        css_folder = os.path.join(static_folder, 'css')
        js_folder = os.path.join(static_folder, 'js')
        img_folder = os.path.join(static_folder, 'img')
        media_folder = os.path.join(static_folder, 'media')
        favicon_path = os.path.join(static_folder, 'favicon.ico')

        if os.path.exists(css_folder):
            shutil.rmtree(css_folder)
            print_success("Deleted css folder.")

        if os.path.exists(js_folder):
            shutil.rmtree(js_folder)
            print_success("Deleted js folder.")

        if os.path.exists(img_folder):
            shutil.rmtree(img_folder)
            print_success("Deleted img folder.")

        # if os.path.exists(media_folder):
        #     clear_folder(media_folder)
        #     print_success("Cleared media folder content.")

        if os.path.exists(favicon_path):
            os.remove(favicon_path)
            print_success("Deleted favicon.ico.")

    except Exception as e:
        print_error(f"Error deleting specific static files: {e}")

    try:
        print_info("Deleting old template files...")
        shutil.rmtree(templates_folder)
        os.makedirs(templates_folder)
        print_success("Deleted all files from templates folder.")
    except Exception as e:
        print_error(f"Error deleting template files: {e}")

    # Move new files
    try:
        print_info("Moving new files to templates folder...")
        shutil.move(os.path.join(dist_folder, 'index.html'), os.path.join(templates_folder, 'index.html'))
        print_success(f"Moved index.html to {templates_folder}.")
    except Exception as e:
        print_error(f"Error moving index.html: {e}")

    try:
        for file in os.listdir(dist_folder):
            if file != "index.html" and file != 'static':
                shutil.move(os.path.join(dist_folder, file), os.path.join(static_folder, file))
                print_success(f"Moved {file} to {static_folder}.")
        print_success("File move completed.")
    except Exception as e:
        print_error(f"Error moving files: {e}")

if __name__ == "__main__":
    build_result = build()
    if build_result:
        move()
    else:
        print_error("Build was not successful. No files were moved.")
