"""
封装系服务监控相关函数
"""
import psutil as psutil


def get_cpu_info():
    """
    获取cpu所有信息
    """
    pass


def get_memory_info():
    """
    获取内存所有信息
    """
    pass


def get_disk_info():
    """
    获取硬盘所有信息
    """
    pass


def get_cpu_used_percent():
    """
    获取CPU运行情况
    :return:
    """
    try:
        return float(psutil.cpu_percent(0.1))
    except:
        pass


def get_memory_used_percent():
    try:
        memory_info = psutil.virtual_memory()
        return float(memory_info.percent)
    except:
        pass


def get_disk_used_percent():
    print(psutil.disk_partitions())
    try:
        return float(psutil.disk_usage("/").percent)
    except:
        pass


if __name__ == '__main__':
    get_disk_used_percent()
