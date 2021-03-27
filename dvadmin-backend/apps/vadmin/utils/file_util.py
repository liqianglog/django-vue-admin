"""
封装文件操作:
  ● 递归读取所有文件目录形成列表
  ● 递归删除空目录
  ● 批量删除文件
"""
import os


def get_all_files(targetDir):
    """
    递归读取所有文件目录形成列表
    :param targetDir:
    :return:
    """
    files = []
    listFiles = os.listdir(targetDir)
    for i in range(0, len(listFiles)):
        path = os.path.join(targetDir, listFiles[i])
        if os.path.isdir(path):
            files.extend(get_all_files(path))
        elif os.path.isfile(path):
            files.append(path)
    return files


def remove_empty_dir(path):
    """
    递归删除空目录
    :param path:
    :return:
    """
    for root, dirs, files in os.walk(path, topdown=False):
        if not files and not dirs:
            os.rmdir(root)


def delete_files(delete_list: list):
    """
    批量删除文件
    :param delete_list:
    :return:
    """
    for file_path in delete_list:
        try:
            os.remove(file_path)
        except(FileNotFoundError):
            pass
