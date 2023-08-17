import os


def generate_tree(directory, prefix="", ignore_dirs=[], ignore_files=[]):
    # 忽略指定的目录和文件
    items = [item for item in os.listdir(directory) if item not in ignore_dirs and item not in ignore_files]
    items = sorted(items)  # 对目录和文件排序

    for i, item in enumerate(items):
        path = os.path.join(directory, item)

        # 确定使用哪个前缀
        is_last_item = i == len(items) - 1
        current_prefix = prefix + ('└── ' if is_last_item else '├── ')
        next_prefix = prefix + ('    ' if is_last_item else '│   ')

        if os.path.isdir(path):
            print(current_prefix + item + '/')
            generate_tree(path, next_prefix, ignore_dirs=ignore_dirs, ignore_files=ignore_files)
        else:
            print(current_prefix + item)


if __name__ == "__main__":
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取项目根目录

    # 要忽略的文件夹和文件
    ignore_dirs = ["__pycache__", ".idea", "venv"]
    ignore_files = []

    print(project_root.split(os.sep)[-1] + "/")
    generate_tree(project_root, ignore_dirs=ignore_dirs, ignore_files=ignore_files)
