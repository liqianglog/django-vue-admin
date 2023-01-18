from django.db import models

from carton_manage.basics.models import CodePackageTemplate
from dvadmin.utils.models import CoreModel

table_prefix = "carton_"

SOURCE=(
    (0,'API同步'),
    (1,"手动导入")
)

VALIDATE_STATUS = (
   (1,"待校验"),
   (2,"校验中"),
   (3,"校验失败"),
   (4,"校验成功")
)

class CodePackage(CoreModel):
    zip_name = models.CharField(max_length=100,blank=True,help_text="压缩包名称",verbose_name="压缩包名称")
    no = models.CharField(max_length=255,unique=True,blank=True,help_text="码包编号",verbose_name="码包编号")
    order_id = models.CharField(max_length=100,blank=True,help_text="订单编号",verbose_name="订单编号")
    product_name = models.CharField(max_length=100, blank=True, help_text="产品名称", verbose_name="产品名称")
    arrival_factory = models.CharField(max_length=100,blank=True,help_text="到货工厂",verbose_name="到货工厂")
    source = models.IntegerField(choices=SOURCE,default=1,blank=True,help_text="来源",verbose_name="来源")
    total_number = models.IntegerField(default=0,blank=True,help_text="码包总数",verbose_name="码包总数")
    code_package_template = models.ForeignKey(CodePackageTemplate,db_constraint=False,on_delete=models.CASCADE,related_name="code_package_template",help_text="码包模板",verbose_name="码包模板")
    validate_status = models.IntegerField(choices=VALIDATE_STATUS,default=1,blank=True,help_text="校验状态",verbose_name="校验状态")
    package_repetition_number = models.IntegerField(default=0,blank=True,help_text="码包重码数",verbose_name="码包重码数")
    database_repetition_number = models.IntegerField(default=0,blank=True,help_text="数据库重码数",verbose_name="数据库重码数")
    import_start_datetime = models.DateTimeField(null=True, blank=True, help_text="导入开始时间", verbose_name="导入开始时间")
    import_end_datetime = models.DateTimeField(null=True, blank=True, help_text="导入结束时间",
                                                 verbose_name="导入结束时间")
    import_run_time = models.DecimalField(max_digits=10,decimal_places=3,default=0,blank=True,help_text="导入耗时",verbose_name="导入耗时")
    import_log = models.JSONField(null=True,blank=True,help_text="导入日志",verbose_name="导入日志")
    is_use = models.BooleanField(default=False,blank=True,help_text="是否被使用",verbose_name="是否被使用")
    file_position = models.CharField(max_length=255,blank=True,null=True,help_text="码包存放位置",verbose_name="码包存放位置")
    file_md5 =  models.CharField(max_length=255,blank=True,null=True,help_text="码包MD5",verbose_name="码包MD5")
    first_line_md5 = models.CharField(max_length=255, blank=True, null=True, help_text="码包首行MD5", verbose_name="码包首行MD5")

    class Meta:
        db_table = table_prefix + "code_package"
        verbose_name = '码包管理'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)

    def __str__(self):
        return str(self.no)


CODE_TYPE = (
    (0,"外码"),
    (1,"内码"),
    (2,"外码+内码")
)
REPETITION_TYPE = (
    (0,"码包重码"),
    (1,"历史重码")
)

class CodeRepetitionRecord(CoreModel):
    code_package = models.ForeignKey(CodePackage,db_constraint=False,on_delete=models.CASCADE,related_name="record",help_text="关联码包",verbose_name="关联码包")
    repetition_code_package = models.ForeignKey(CodePackage,db_constraint=False,on_delete=models.CASCADE,related_name="repetition",help_text="关联被重码码包",verbose_name="关联被重码码包")
    code_content = models.CharField(max_length=255,help_text="码内容",verbose_name="码内容")
    code_content_md5 = models.CharField(max_length=255,help_text="码内容MD5",verbose_name="码内容MD5")
    code_type = models.IntegerField(choices=CODE_TYPE, help_text="码类型", verbose_name="码类型")
    repetition_type = models.IntegerField(choices=REPETITION_TYPE, help_text="码类型", verbose_name="码类型")
    class Meta:
        db_table = table_prefix + "code_repetition_record"
        verbose_name = '重码记录'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)