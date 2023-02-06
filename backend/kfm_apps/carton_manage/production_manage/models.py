from django.db import models
from basics_manage.models import DeviceManage, ProductionLine, FactoryInfo
from dvadmin.utils.models import CoreModel
from carton_manage.code_manage.models import CodePackage

table_prefix = "carton_"

WORK_STATUS = (
    (0, "待下载"),
    (1, "待生产"),
    (2, "生产中"),
    (3, "暂停中"),
    (4, "结束生产"),
    (5, "工单异常")
)


class ProductionWork(CoreModel):
    code_package = models.ForeignKey(CodePackage, db_constraint=False, on_delete=models.PROTECT,
                                     related_name="work_code_package", help_text="关联码包", verbose_name="关联码包")
    no = models.CharField(max_length=200, help_text="工单编号", verbose_name="工单编号")
    order_id = models.CharField(max_length=100, blank=True, help_text="订单编号", verbose_name="订单编号")
    batch_no = models.CharField(max_length=100, null=True, blank=True, help_text="批次号", verbose_name="批次号")
    device = models.ForeignKey(DeviceManage, db_constraint=False, on_delete=models.CASCADE, related_name="prod_device",
                               help_text="关联设备", verbose_name="关联设备")
    production_line = models.ForeignKey(ProductionLine, db_constraint=False, on_delete=models.PROTECT,
                                        related_name="prod_production_line", help_text="关联产线",
                                        verbose_name="关联产线")
    factory_info = models.ForeignKey(FactoryInfo, db_constraint=False, on_delete=models.PROTECT,
                                     related_name="prod_factory", help_text="关联工厂", verbose_name="关联工厂")
    print_position = models.IntegerField(default=0, blank=True, help_text="打印位置", verbose_name="打印位置")
    print_last_datetime = models.DateTimeField(null=True, blank=True, help_text="最后打印时间",
                                               verbose_name="最后打印时间")
    status = models.IntegerField(choices=WORK_STATUS, default=0, blank=True, help_text="生产状态",
                                 verbose_name="生产状态")

    class Meta:
        db_table = table_prefix + "production_work"
        verbose_name = '生产工单'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class ProductionWorkStatusRecord(models.Model):
    production_work = models.ForeignKey(ProductionWork, db_constraint=False, on_delete=models.PROTECT,
                                     related_name="status_record_prod_work", help_text="关联生产工单", verbose_name="关联生产工单")
    status = models.IntegerField(choices=WORK_STATUS, default=0, blank=True, help_text="生产状态",
                                 verbose_name="生产状态")
    print_position = models.IntegerField(default=0, blank=True, help_text="打印位置", verbose_name="打印位置")
    record_datetime = models.DateTimeField(auto_now_add=True,blank=True,verbose_name="记录时间",help_text="记录时间")

    class Meta:
        db_table = table_prefix + "production_work_status_record"
        verbose_name = '生产工单状态记录'
        verbose_name_plural = verbose_name

VERIFY_RESULT = (
    (0,"失败"),
    (1,"成功")
)
class ProductionWorkVerifyRecord(models.Model):
    production_work = models.ForeignKey(ProductionWork, db_constraint=False, on_delete=models.PROTECT,
                                        related_name="verify_record_prod_work", help_text="关联生产工单",
                                        verbose_name="关联生产工单")
    code_list = models.JSONField(verbose_name="码数据集合",help_text="码数据集合")
    result = models.IntegerField(default=1,choices=VERIFY_RESULT, blank=True, help_text="验证结果", verbose_name="验证结果")
    remark = models.CharField(max_length=255,blank=True,null=True,verbose_name="备注",help_text='备注')
    record_datetime = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="记录时间", help_text="记录时间")

    class Meta:
        db_table = table_prefix + "production_work_verify_record"
        verbose_name = '生产工单生产校验记录'
        verbose_name_plural = verbose_name


class CodePackageDownloadRecord(models.Model):
    production_work = models.ForeignKey(ProductionWork, db_constraint=False, on_delete=models.PROTECT,
                                        related_name="codepackage_download_prod_work", help_text="关联生产工单",
                                        verbose_name="关联生产工单")
    record_datetime = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="记录时间", help_text="记录时间")
    download_ip = models.CharField(max_length=255,verbose_name="下载IP",help_text="下载IP")
    device = models.ForeignKey(DeviceManage, db_constraint=False, on_delete=models.PROTECT,
                                        related_name="download_device", help_text="关联设备",
                                        verbose_name="关联设备")
    header_range = models.CharField(max_length=255,null=True,blank=True,verbose_name="请求头Range",help_text="请求头Range")

    class Meta:
        db_table = table_prefix + "code_package_download_record"
        verbose_name = '码包下载记录'
        verbose_name_plural = verbose_name
