from utils import fields
from utils.BaseModels import CoreModel


class Post(CoreModel):
    name = fields.CharField(null=False, max_length=64, verbose_name="岗位名称")
    web_path = fields.CharField(max_length=32, verbose_name="岗位编码")
    orderNum = fields.IntegerField(verbose_name="岗位顺序")
    status = fields.BooleanField(default=False, verbose_name="岗位状态")
    remark = fields.TextField(verbose_name="备注", help_text="备注")

    class Meta:
        verbose_name = '岗位管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"
