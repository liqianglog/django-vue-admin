import logging

from django.db.models import Model
from rest_framework.request import Request
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class ViewLogger(object):
    """
    基于View视图的日志
    """

    def __init__(self, view=None, request=None, *args, **kwargs) -> None:
        super().__init__()
        self.view = view
        self.request = request
        self.model = None
        self.log_prefix: str = ''
        if self.view and hasattr(self.view.get_queryset(), 'model'):
            self.model: Model = self.view.get_queryset().model
        elif self.view and hasattr(self.view.get_serializer(), 'Meta') and hasattr(self.view.get_serializer().Meta,
                                                                                   'model'):
            self.model: Model = self.view.get_serializer().Meta.model
        if self.model:
            request.session['model_name'] = str(getattr(self.model, '_meta').verbose_name)

    def handle(self, request: Request, *args, **kwargs):
        pass

    def logger(self, msg):
        """

        :param msg:
        :return: logger
        """
        self.request.session['request_msg'] = msg
        return logger


class APIViewLogger(ViewLogger):
    """
    (1)仅在op_drf.views.CustomAPIView的子类中生效
    (2)使用: 请勿直接配置view_logger_classes = (APIViewLogger, ), 这样无效,
             如有需求, 需要继承APIViewLogger重写其相应的方法
    (3)重写handle()方法,所有请求均触发此方法
       重写handle_get()方法,仅GET请求均触发此方法
       重写handle_post()方法,仅POST请求均触发此方法
       重写handle_put()方法,仅PUT请求均触发此方法
       重写handle_delete()方法,仅DELETE请求均触发此方法
       重写handle_xxx()方法,仅xxx请求均触发此方法
    """

    def __init__(self, view=None, request=None, *args, **kwargs) -> None:
        super().__init__(view, request, *args, **kwargs)
        self.view: APIView = view
        self.request: Request = request
        self.user = request.user


class ModelViewLogger(APIViewLogger):
    """
    基础模型操作日志
    (1)仅在op_drf.viewsets.GenericViewSet的子类中生效
    (1)在CustomModelViewSet子类中配置: view_logger_classes = [ModelViewLogger, ]
    (2)不要在op_drf中继续写具体的日志逻辑代码,
       如有需求, 应该继承ModelViewLogger并且重写相应的方法, 例如CustomerModelViewLogger(涉及到其他模块时不要将代码放入op_drf)
    """

    def __init__(self, view=None, request=None, *args, **kwargs) -> None:
        super().__init__(view, request, *args, **kwargs)


class RelationshipViewLogger(APIViewLogger):
    """
    关联关系模型操作日志
    (1)在ModelRelationshipView子类中配置: view_logger_classes = [RelationshipViewLogger, ]
    (2)不要在op_drf中继续写具体的日志逻辑代码,
       如有需求, 应该继承RelationshipViewLogger并且重写相应的方法, 例如CustomerRelationshipViewLogger(涉及到其他模块时不要将代码放入op_drf)
    """

    def __init__(self, view=None, request=None, instanceId=None, *args, **kwargs) -> None:
        super().__init__(view, request)
        self.instanceId: str = instanceId

    def handle(self, request: Request, *args, **kwargs):
        """
        每一次请求都会触发此方法
        """

    pass


class CustomerRelationshipViewLogger(RelationshipViewLogger):
    """
    (1)在ModelRelationshipView子类中配置: view_logger_classes = [CustomerRelationshipViewLogger, ]
    """

    def __init__(self, view=None, request=None, instanceId=None, *args, **kwargs) -> None:
        super().__init__(view, request, instanceId, *args, **kwargs)
        self.log_prefix: str = 'RelationshipView日志系统:'

    def handle_get(self, request: Request, *args, **kwargs):
        """
        仅GET请求才会触发此方法
        """
        pass

    def handle_post(self, request: Request, *args, **kwargs):
        """
        仅POST请求才会触发此方法
        """
        operator = self.user.username
        model_name = getattr(self.view.model, '_meta').verbose_name
        to_field_name = self.view.to_field_name
        to_model_name = getattr(self.view.relationship_model, '_meta').verbose_name
        self.logger(
            f'{self.log_prefix}用户[username={operator}]新增, {model_name}实例[{to_field_name}={self.instanceId}]与{to_model_name}的关联关系')

    def handle_put(self, request: Request, *args, **kwargs):
        """
        仅PUT请求才会触发此方法
        """
        operator = self.user.username
        model_name = getattr(self.view.model, '_meta').verbose_name
        to_field_name = self.view.to_field_name
        to_model_name = getattr(self.view.relationship_model, '_meta').verbose_name
        self.logger(
            f'{self.log_prefix}用户[username={operator}]重置, {model_name}实例[{to_field_name}={self.instanceId}]与{to_model_name}的关联关系')

    def handle_delete(self, request: Request, *args, **kwargs):
        """
        仅DELETE请求才会触发此方法
        """
        operator = self.user.username
        model_name = getattr(self.view.model, '_meta').verbose_name
        to_field_name = self.view.to_field_name
        to_model_name = getattr(self.view.relationship_model, '_meta').verbose_name
        self.logger(
            f'{self.log_prefix}用户[username={operator}]移除, {model_name}实例[{to_field_name}={self.instanceId}]与{to_model_name}的关联关系')


class CustomerModelViewLogger(ModelViewLogger):
    def __init__(self, view=None, request=None, *args, **kwargs) -> None:
        super().__init__(view, request, *args, **kwargs)
        self.log_prefix: str = 'CustomModelViewSet日志系统:'

    def handle(self, request: Request, *args, **kwargs):
        pass

    def handle_retrieve(self, request: Request, instance: Model = None, *args, **kwargs):
        """
        仅retrieve(GET)请求才会触发此方法
        """
        pass
        operator = self.user.username
        model_name = getattr(self.model, '_meta').verbose_name
        self.logger(f'{self.log_prefix}用户[username={operator}]检索{model_name}:[{instance}]')

    def handle_list(self, request: Request, *args, **kwargs):
        """
        仅list(GET)请求才会触发此方法
        """
        pass
        operator = self.user.username
        model_name = getattr(self.model, '_meta').verbose_name
        self.logger(f'{self.log_prefix}用户[username={operator}]查询{model_name}')

    def handle_create(self, request: Request, instance: Model = None, *args, **kwargs):
        """
        仅create(POST)请求才会触发此方法
        """
        pass
        operator = self.user.username
        model_name = getattr(self.model, '_meta').verbose_name
        self.logger(f'{self.log_prefix}用户[username={operator}]创建{model_name}:[{instance}]')

    def handle_update(self, request: Request, instance: Model = None, *args, **kwargs):
        """
        仅update(PUT)请求才会触发此方法
        """
        pass
        operator = self.user.username
        model_name = getattr(self.model, '_meta').verbose_name
        self.logger(f'{self.log_prefix}用户[username={operator}]更新{model_name}:[{instance}]')

    def handle_partial_update(self, request: Request, instance: Model = None, *args, **kwargs):
        """
        仅partial_update(PATCH)请求才会触发此方法
        """
        pass
        operator = self.user.username
        model_name = getattr(self.model, '_meta').verbose_name
        self.logger(f'{self.log_prefix}用户[username={operator}]部分更新{model_name}:[{instance}]')

    def handle_destroy(self, request: Request, instance: Model = None, *args, **kwargs):
        """
        仅destroy(DELETE)请求才会触发此方法
        """
        pass
        operator = self.user.username
        model_name = getattr(self.model, '_meta').verbose_name
        self.logger(f'{self.log_prefix}用户[username={operator}]删除{model_name}:[{instance}]')

    def handle_other(self, request: Request, instance: Model = None, *args, **kwargs):
        """
        仅 其他 请求才会触发此方法
        """
        pass
        operator = self.user.username
        model_name = getattr(self.model, '_meta').verbose_name
        self.logger(f'{self.log_prefix}用户[username={operator}]其他请求{model_name}:[{instance}]')
