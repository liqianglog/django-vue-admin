from django.db import models

from basics_manage.models import DeviceManage, CodePackageFormat
from carton_manage.production_manage.models import ProductionWork
from dvadmin.utils.models import CoreModel

table_prefix = "carton_"
CODE_TYPE_STATUS = (
    (0, "外码"),
    (1, "内码"),
    (2, "外码+内码")
)

class CameraManage(CoreModel):
    no = models.CharField(max_length=100, unique=True, help_text="编号", verbose_name="编号")
    device = models.ForeignKey(DeviceManage,db_constraint=False,related_name='cam_device',on_delete=models.CASCADE,verbose_name="关联设备",help_text="关联设备")

    class Meta:
        db_table = table_prefix + "camera_manage"
        verbose_name = '检测相机管理'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class BackHaulFile(CoreModel):
    production_work = models.ForeignKey(ProductionWork, db_constraint=False, on_delete=models.PROTECT,
                                        related_name="bhfile_prod_work", help_text="关联生产工单",
                                        verbose_name="关联生产工单")
    code_type = models.IntegerField(choices=CODE_TYPE_STATUS, default=1, blank=True, help_text="码类型",
                                    verbose_name="码类型")
    device = models.ForeignKey(DeviceManage, db_constraint=False, related_name='bhfile_device', on_delete=models.CASCADE,
                               verbose_name="关联设备", help_text="关联设备")
    cam = models.ForeignKey(CameraManage, db_constraint=False, related_name='bhfile_cam', on_delete=models.CASCADE,
                               verbose_name="关联相机", help_text="关联相机")
    total_number = models.IntegerField(default=0, blank=True, help_text="码总数", verbose_name="码总数")
    success_number  = models.IntegerField(default=0, blank=True, help_text="识别成功数", verbose_name="识别成功数")
    error_number  = models.IntegerField(default=0, blank=True, help_text="识别成功数", verbose_name="识别成功数")
    file_position = models.CharField(max_length=255, blank=True, null=True, help_text="码包存放位置",
                                     verbose_name="码包存放位置")
    file_md5 = models.CharField(max_length=255, blank=True, null=True, help_text="文件MD5", verbose_name="文件MD5")
    key_id = models.IntegerField(default=0, blank=True, help_text="加密ID索引", verbose_name="加密ID索引")
    code_package_format = models.ForeignKey(CodePackageFormat, db_constraint=False, related_name='bhfile_code_package_format', on_delete=models.CASCADE,
                            verbose_name="关联码包回传格式", help_text="关联码包回传格式")
    class Meta:
        db_table = table_prefix + "back_haul_file"
        verbose_name = '回传文件管理'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)

ERROR_TYPE = (
    (0,"未识别"),
    (1,'正常'),
    (2,'码不存在'),
    (3,'本码包重码'),
    (4,'历史码重码'),
    (5,'非生产工单码')
)
class VerifyCodeRecord(CoreModel):
    back_haul_file = models.ForeignKey(BackHaulFile, db_constraint=False, on_delete=models.PROTECT,
                                        related_name="verify_code_bhfile", help_text="关联生产工单",
                                        verbose_name="关联回传文件管理")
    code_content = models.CharField(max_length=255, help_text="码内容", verbose_name="码内容")
    code_type = models.IntegerField(choices=CODE_TYPE_STATUS, default=1, blank=True, help_text="码类型",
                                    verbose_name="码类型")
    ac_time = models.DateTimeField(auto_now_add=True,null=True,blank=True,verbose_name="采集时间",help_text="采集时间")
    rep_code_number = models.IntegerField(null=True,blank=True,default=0,verbose_name="重码次数",help_text="重码次数")
    error_type = models.IntegerField(choices=ERROR_TYPE, default=1, blank=True, help_text="问题码类型",
                                    verbose_name="问题码类型")

    class Meta:
        db_table = table_prefix + "verify_code_record"
        verbose_name = '校验码记录'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)

class ErrorCodeRecord(CoreModel):
    verify_code_record = models.ForeignKey(VerifyCodeRecord, db_constraint=False, on_delete=models.PROTECT,
                                       related_name="error_code_verify", help_text="关联校验码记录",
                                       verbose_name="关联校验码记录")
    ac_time = models.DateTimeField(auto_now_add=True,null=True, blank=True,verbose_name="采集时间", help_text="采集时间")

    class Meta:
        db_table = table_prefix + "error_code_record"
        verbose_name = '错误码记录'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)