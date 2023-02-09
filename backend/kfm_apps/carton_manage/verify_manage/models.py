from django.db import models
from psqlextra.indexes import UniqueIndex
from psqlextra.models import PostgresPartitionedModel
from psqlextra.types import PostgresPartitioningMethod

from basics_manage.models import DeviceManage, CodePackageFormat
from carton_manage.production_manage.models import ProductionWork
from dvadmin.utils.models import CoreModel, AddPostgresPartitionedBase
from dvadmin_tenants.models import HistoryCodeInfo

table_prefix = "carton_"
CODE_TYPE_STATUS = (
    (0, "内码"),
    (1, "外码"),
    (2, "未知")
)


class CameraManage(CoreModel):
    no = models.CharField(max_length=100, unique=True, help_text="编号", verbose_name="编号")
    device = models.ForeignKey(DeviceManage, db_constraint=False, related_name='cam_device', on_delete=models.CASCADE,
                               verbose_name="关联设备", help_text="关联设备")

    class Meta:
        db_table = table_prefix + "camera_manage"
        verbose_name = '检测相机管理'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class BackHaulFile(CoreModel):
    production_work = models.ForeignKey(ProductionWork, db_constraint=False, on_delete=models.PROTECT,
                                        related_name="bhfile_prod_work", help_text="关联生产工单",
                                        verbose_name="关联生产工单")
    code_type = models.IntegerField(choices=CODE_TYPE_STATUS, default=3, blank=True, help_text="码类型",
                                    verbose_name="码类型")
    device = models.ForeignKey(DeviceManage, db_constraint=False, related_name='bhfile_device',
                               on_delete=models.CASCADE,
                               verbose_name="关联设备", help_text="关联设备")
    cam = models.ForeignKey(CameraManage, db_constraint=False, related_name='bhfile_cam', on_delete=models.CASCADE,
                            verbose_name="关联相机", help_text="关联相机")
    total_number = models.IntegerField(default=0, blank=True, help_text="码总数", verbose_name="码总数")
    success_number = models.IntegerField(default=0, blank=True, help_text="识别成功数", verbose_name="识别成功数")
    error_number = models.IntegerField(default=0, blank=True, help_text="识别错误数", verbose_name="识别错误数")
    file_position = models.CharField(max_length=255, blank=True, null=True, help_text="码包存放位置",
                                     verbose_name="码包存放位置")
    file_md5 = models.CharField(max_length=255, blank=True, null=True, help_text="文件MD5", verbose_name="文件MD5")
    key_id = models.IntegerField(default=0, blank=True, help_text="加密ID索引", verbose_name="加密ID索引")
    code_package_format = models.ForeignKey(CodePackageFormat, db_constraint=False,
                                            related_name='bhfile_code_package_format', on_delete=models.CASCADE,
                                            verbose_name="关联码包回传格式", help_text="关联码包回传格式")
    @classmethod
    def update_result(cls, back_haul_file_id):
        obj = cls.objects.get(id=back_haul_file_id)
        VerifyCodeRecord.objects.filter(production_work_no=obj.production_work.no)
        pass
        # TODO 更新回传文件内容

    class Meta:
        db_table = table_prefix + "back_haul_file"
        verbose_name = '回传文件管理'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


ERROR_TYPE = (
    (0, "未识别"),
    (1, '正常'),
    (2, '码不存在'),
    (3, '本检测包重码'),
    (4, '本生产工单重码'),
    (5, '非本生产工单码')
)


class VerifyCodeRecord(PostgresPartitionedModel, AddPostgresPartitionedBase, CoreModel):
    """
    使用分表
    """
    production_work_no = models.CharField(max_length=200, help_text="生产工单编号", verbose_name="生产工单编号")
    back_haul_file = models.ForeignKey(BackHaulFile, db_constraint=False, on_delete=models.PROTECT,
                                       related_name="verify_code_bhfile", help_text="关联生产工单",
                                       verbose_name="关联回传文件管理")
    code_content_md5 = models.CharField(max_length=255, help_text="码内容", verbose_name="码内容")
    error_code_content = models.CharField(max_length=255, null=True, blank=True, help_text="异常明码码内容",
                                          verbose_name="异常明码码内容")
    code_type = models.IntegerField(choices=CODE_TYPE_STATUS, default=1, blank=True, help_text="码类型",
                                    verbose_name="码类型")
    ac_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="采集时间",
                                   help_text="采集时间")
    error_type = models.IntegerField(choices=ERROR_TYPE, default=1, blank=True, help_text="问题码类型",
                                     verbose_name="问题码类型")
    rep_code_id = models.CharField(max_length=200, help_text="关联被重复码id", verbose_name="关联被重复码id")
    rep_package_id = models.CharField(max_length=200, help_text="被重码码包id", verbose_name="被重码码包id")
    rep_tenant_id = models.CharField(max_length=200, help_text="被重码生产工单编号", verbose_name="被重码生产工单编号")

    class Meta:
        db_table = table_prefix + "verify_code_record"
        verbose_name = '校验码记录'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)
        indexes = [
            UniqueIndex(fields=['production_work_no', 'create_datetime']),
        ]

    @classmethod
    def ck_verify_code(cls, data: dict, package_id):
        """
        data:{
            md5_value: {
                {"code_content": code_content, "ac_time": ac_time}
            },
        }
        return {
                "error_type_1": {},  # 正常码包
                "error_type_2": { # 码不存在
                    md5_value: {
                        "code_type": 0,  # 0 内码; 1 外码
                        "tenant_id": 100001,
                        "package_id": xxx,
                    }
                },
                "error_type_3": { # 本检测包重码
                    md5_value: {
                        "code_type": 0,  # 0 内码; 1 外码
                        "tenant_id": 100001,
                        "package_id": xxx
                    }
                },
                "error_type_4": {  # 本生产工单重码
                    md5_value: {
                        "code_type": 0,  # 0 内码; 1 外码
                        "tenant_id": 100001,
                        "package_id": xxx,
                        "rep_code_id": rep_code_id,
                        "rep_package_id": rep_package_id,
                        "rep_tenant_id": rep_tenant_id,
                    }
                },
                "error_type_5": {  # 非本生产工单码
                    md5_value: {
                        "code_type": 0,  # 0 内码; 1 外码
                        "tenant_id": 100001,
                        "package_id": xxx,
                        "rep_code_id": rep_code_id,
                        "rep_package_id": rep_package_id,
                        "rep_tenant_id": rep_tenant_id,
                    }
                },
            }
        """
        if not data:
            return {
                "error_type_1": {},  # 正常码包
                "error_type_2": {},  # 码不存在
                "error_type_3": {},  # 本检测包重码
                "error_type_4": {},  # 本生产工单重码
                "error_type_5": {},  # 非本生产工单码
            }
        # 1. 检测本数据data中是否有重码 (3)
        _HistoryCodeInfo = HistoryCodeInfo.set_db()
        select_data = _HistoryCodeInfo.select_data_duplicate(data.keys(), package_id)
        # 2. 查询不在本码包中的码 (5)
        # 3. 不在本码包中返回的值，重新进行ck全表查询，判断是否全局存在 (2)
        # 4. 通过 verify_code_record 表查询本生产工单中是否有重码 (4)
        # 5. 剩余正常码包返回 (1)

        return {
            "error_type_1": {},  # 正常码包
            "error_type_2": {},  # 码不存在
            "error_type_3": {},  # 本检测包重码
            "error_type_4": {},  # 本生产工单重码
            "error_type_5": {},  # 非本生产工单码
        }

    class PartitioningMeta:
        method = PostgresPartitioningMethod.LIST
        key = ["production_work_no"]
