from config import environment_config


if environment_config == 'sit':
    from conf.sit import *
elif environment_config == 'prod':
    from conf.prod import *
else :
    from conf.env import *
print(f"导入[{environment_config}]配置成功！")
