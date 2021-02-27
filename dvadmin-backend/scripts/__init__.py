import os


def getSql(filename):
    """
    获取文件内所有sql
    :param filename: 例如：os.path.join('permission','permission_dept.sql')
    :return:
    """
    pwd = os.path.join(os.getcwd(), 'scripts', filename)
    with open(pwd) as fp:
        content = fp.read()
    return [ele for ele in content.split('\n') if not ele.startswith('--') and ele]
