import os


def getSql(filename):
    """
    获取文件内所有sql
    :param filename: 例如：os.path.join('permission','permission_dept.sql')
    :return:
    """
    pwd = os.path.join(os.getcwd(), 'scripts', filename)
    with open(pwd,'rb') as fp:
        content = fp.read().decode('utf8')
    return [ele for ele in content.split('\n') if not ele.startswith('--') and ele]
