from django.dispatch import Signal
# 初始化信号
pre_init_complete = Signal(providing_args=['msg', 'data'])
detail_init_complete = Signal(providing_args=['msg', 'data'])
post_init_complete = Signal(providing_args=['msg', 'data'])
# 租户初始化信号
pre_tenants_init_complete = Signal(providing_args=['msg', 'data'])
detail_tenants_init_complete = Signal(providing_args=['msg', 'data'])
post_tenants_init_complete = Signal(providing_args=['msg', 'data'])
post_tenants_all_init_complete = Signal(providing_args=['msg', 'data'])
# 租户创建完成信号
tenants_create_complete = Signal(providing_args=['msg', 'data'])
