from django.db import models

from carton_manage.basics_manage.models import Device, ProductionLine, FactoryInfo
from carton_manage.code_manage.models import CodePackage
from dvadmin.utils.models import CoreModel

table_prefix = "carton_"

WORK_STATUS = (
(0,"待下载")
,(1,"待生产")
,(2,"生产中")
,(3,"暂停中")
,(4,"结束生产")
,(5,"工单异常")
)

class ProductionWork(CoreModel):
    code_package = models.ForeignKey(CodePackage, db_constraint=False, on_delete=models.CASCADE, related_name="work_code_package",
                                     help_text="关联码包", verbose_name="关联码包")
    no = models.CharField(max_length=200,help_text="工单编号",verbose_name="工单编号")
    order_id = models.CharField(max_length=100, blank=True, help_text="订单编号", verbose_name="订单编号")
    batch_no = models.CharField(max_length=100, null=True,blank=True, help_text="批次号", verbose_name="批次号")
    device = models.ForeignKey(Device,db_constraint=False,on_delete=models.CASCADE,related_name="prod_device",help_text="关联设备",verbose_name="关联设备")
    production_line = models.ForeignKey(ProductionLine, db_constraint=False, on_delete=models.CASCADE, related_name="prod_production_line",
                               help_text="关联产线", verbose_name="关联产线")
    factory_info = models.ForeignKey(FactoryInfo, db_constraint=False, on_delete=models.CASCADE,
                                        related_name="prod_factory",
                                        help_text="关联工厂", verbose_name="关联工厂")
    print_position = models.IntegerField(default=0,blank=True,help_text="打印位置",verbose_name="打印位置")
    print_last_datetime = models.DateTimeField(null=True,blank=True,help_text="最后打印时间",verbose_name="最后打印时间")
    status = models.IntegerField(choices=WORK_STATUS,default=0,blank=True,help_text="生产状态",verbose_name="生产状态")
    class Meta:
        db_table = table_prefix + "production_work"
        verbose_name = '生产工单'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)
