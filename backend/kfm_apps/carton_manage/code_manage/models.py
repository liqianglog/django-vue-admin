import datetime
import json
import os
import shutil

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils import timezone

from dvadmin.utils.models import CoreModel
from basics_manage.models import CodePackageTemplate, DeviceManage, ProductInfo, CustomerInfo, FactoryInfo
from utils.currency import get_code_package_import_txt_path, zip_compress_file, des_encrypt_file, md5_file, \
    get_code_package_import_fail_path

table_prefix = "carton_"

SOURCE = (
    (0, 'API同步'),
    (1, "手动导入")
)

VALIDATE_STATUS = (
    (1, "待校验"),
    (2, "校验中"),
    (3, "校验失败"),
    (4, "校验成功")
)

CODE_TYPE_STATUS = (
    (0, "外码"),
    (1, "内码"),
    (2, "外码+内码")
)


class CodePackage(CoreModel):
    zip_name = models.CharField(max_length=100, blank=True, help_text="压缩包名称", verbose_name="压缩包名称")
    no = models.CharField(max_length=255, unique=True, blank=True, help_text="码包编号", verbose_name="码包编号")
    order_id = models.CharField(max_length=100, blank=True, help_text="订单编号", verbose_name="订单编号")
    product_info = models.ForeignKey(ProductInfo, db_constraint=False, on_delete=models.PROTECT, help_text="关联产品",
                                     verbose_name="关联产品")
    customer_info = models.ForeignKey(CustomerInfo, db_constraint=False, on_delete=models.PROTECT, help_text="关联客户",
                                      verbose_name="关联客户")
    factory_info = models.ForeignKey(FactoryInfo, db_constraint=False, on_delete=models.PROTECT, help_text="生产工厂",
                                     verbose_name="生产工厂")
    source = models.IntegerField(choices=SOURCE, default=1, blank=True, help_text="来源", verbose_name="来源")

    code_package_template = models.ForeignKey(CodePackageTemplate, db_constraint=False, on_delete=models.PROTECT,
                                              related_name="code_package_template", help_text="码包模板",
                                              verbose_name="码包模板")
    validate_status = models.IntegerField(choices=VALIDATE_STATUS, default=1, blank=True, help_text="校验状态",
                                          verbose_name="校验状态")
    # 根据关联客户携带出
    attribute_fields = models.JSONField(null=True, blank=True, help_text="其他字段属性", verbose_name="其他字段属性")
    # 自动匹配字段
    total_number = models.IntegerField(default=0, blank=True, help_text="码包总数", verbose_name="码包总数")
    key_id = models.IntegerField(default=0, blank=True, help_text="加密ID索引", verbose_name="加密ID索引")
    package_repetition_number = models.IntegerField(default=0, blank=True, help_text="码包重码数",
                                                    verbose_name="码包重码数")
    database_repetition_number = models.IntegerField(default=0, blank=True, help_text="数据库重码数",
                                                     verbose_name="数据库重码数")
    import_start_datetime = models.DateTimeField(null=True, blank=True, help_text="导入开始时间",
                                                 verbose_name="导入开始时间")
    import_end_datetime = models.DateTimeField(null=True, blank=True, help_text="导入结束时间",
                                               verbose_name="导入结束时间")
    import_run_time = models.DecimalField(max_digits=10, decimal_places=3, default=0, blank=True, help_text="导入耗时",
                                          verbose_name="导入耗时")
    import_log = models.JSONField(null=True, blank=True, help_text="导入日志", verbose_name="导入日志")
    device_manage = models.ForeignKey(DeviceManage, db_constraint=False, blank=True, null=True,
                                      on_delete=models.PROTECT, help_text="被生产设备", verbose_name="被生产设备")
    file_position = models.CharField(max_length=255, blank=True, null=True, help_text="码包存放位置",
                                     verbose_name="码包存放位置")
    file_md5 = models.CharField(max_length=255, blank=True, null=True, help_text="码包MD5", verbose_name="码包MD5")
    des_file_md5 = models.CharField(max_length=255, blank=True, null=True, help_text="DES码包MD5",
                                    verbose_name="DES码包MD5")
    first_line_md5 = models.CharField(max_length=255, blank=True, null=True, help_text="码包首行MD5",
                                      verbose_name="码包首行MD5")

    class Meta:
        db_table = table_prefix + "code_package"
        verbose_name = '码包管理'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)

    def __str__(self):
        return str(self.no)

    def write_log(self, obj: dict, package_repetition_number=None, database_repetition_number=None):
        """
        写入日志
        :param obj:  {
            "content": 'xxxx',
            "timestamp": '2023-01-01 00:00:00',
            "type": 'success' # error
        }
        :return:
        """
        if not obj.get('timestamp', None):
            obj['timestamp'] = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        if not obj.get('remark', None):
            obj['remark'] = '-'
        if not obj.get('type', None):
            obj['type'] = 'success'
        obj['result'] = '校验通过' if obj['type'] == 'success' else '校验失败'

        with cache.lock(key="write_log"):
            code_package_obj = CodePackage.objects.get(id=self.id)
            log = (code_package_obj.import_log and json.loads(code_package_obj.import_log)) or []
            log.append(obj)
            code_package_obj.import_log = json.dumps(log)
            if obj.get('type') != 'success':
                code_package_obj.validate_status = 3
                # 对失败的数据进行加密并删除源数据
                source_file_path = os.path.join(get_code_package_import_txt_path(), code_package_obj.file_position)
                target_file_path = source_file_path.replace('.txt', '.zip')
                zip_compress_file(source_file_path, target_file_path, is_rm=True)
                des_encrypt_file(target_file_path, settings.ENCRYPTION_KEY_ID[code_package_obj.key_id])
                os.rename(target_file_path, target_file_path.replace('.zip', '.zip.des'))
                code_package_obj.des_file_md5 = md5_file(
                    os.path.join(get_code_package_import_txt_path(), target_file_path.replace('.zip', '.zip.des')))
                date_strf_time = timezone.now().strftime("%Y%m%d%H%M%S")
                new_file_position = code_package_obj.file_position.replace('.txt', f'_{date_strf_time}.zip.des')
                code_package_obj.file_position = new_file_position
                # 移动文件到指定目录
                to_file = os.path.join(get_code_package_import_fail_path(), new_file_position)
                if not os.path.exists(os.path.join(get_code_package_import_fail_path(),
                                                   *new_file_position.split(os.sep)[:-1])):  # 文件夹不存在则创建
                    os.makedirs(
                        os.path.join(get_code_package_import_fail_path(), *new_file_position.split(os.sep)[:-1]))
                shutil.move(target_file_path.replace('.zip', '.zip.des'), to_file)
                # 把no重新进行命名
                code_package_obj.no = f"{code_package_obj.no}_{date_strf_time}"
            # 本码包重码数量
            if package_repetition_number:
                code_package_obj.package_repetition_number = package_repetition_number
            # 历史码包重码数量
            if database_repetition_number:
                code_package_obj.database_repetition_number = database_repetition_number
            if code_package_obj.import_start_datetime:
                import_end_datetime = datetime.datetime.now()
                code_package_obj.import_end_datetime = import_end_datetime
                code_package_obj.import_run_time = (
                        import_end_datetime - code_package_obj.import_start_datetime).seconds
            code_package_obj.save()


CODE_TYPE = (
    (0, "内码"),
    (1, "外码"),
)
REPETITION_TYPE = (
    (0, "码包重码"),
    (1, "历史重码")
)


class CodeRepetitionRecord(CoreModel):
    code_package = models.ForeignKey(CodePackage, db_constraint=False, on_delete=models.CASCADE, related_name="record",
                                     help_text="关联码包", verbose_name="关联码包")
    repetition_code_package = models.ForeignKey(CodePackage, db_constraint=False, on_delete=models.CASCADE,
                                                related_name="repetition", help_text="关联被重码码包",
                                                verbose_name="关联被重码码包")
    code_content = models.CharField(max_length=255, help_text="码内容", verbose_name="码内容")
    code_content_md5 = models.CharField(max_length=255, help_text="码内容MD5", verbose_name="码内容MD5")
    code_type = models.IntegerField(choices=CODE_TYPE, help_text="码类型", verbose_name="码类型")
    repetition_type = models.IntegerField(choices=REPETITION_TYPE, help_text="重码类型", verbose_name="重码类型")

    class Meta:
        db_table = table_prefix + "code_repetition_record"
        verbose_name = '重码记录'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)
