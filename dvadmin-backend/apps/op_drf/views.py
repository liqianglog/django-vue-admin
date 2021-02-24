import logging
import traceback
from types import FunctionType, MethodType

from rest_framework.exceptions import APIException as DRFAPIException
from rest_framework.request import Request
from rest_framework.views import APIView

from utils import exceptions
from utils.model_util import ModelRelateUtils
from .logging.view_logger import CustomerRelationshipViewLogger
from .response import SuccessResponse, ErrorResponse
from .serializers import CustomModelSerializer

logger = logging.getLogger(__name__)


def op_exception_handler(ex, context):
    """
    统一异常拦截处理
    目的:(1)取消所有的500异常响应,统一响应为标准错误返回
        (2)准确显示错误信息
    :param ex:
    :param context:
    :return:
    """
    msg = ''
    if isinstance(ex, DRFAPIException):
        # set_rollback()
        msg = ex.detail
    elif isinstance(ex, exceptions.APIException):
        msg = ex.message
    elif isinstance(ex, Exception):
        logger.error(traceback.format_exc())
        msg = str(ex)
    return ErrorResponse(msg=msg)


class CustomAPIView(APIView):
    """
    继承、增强DRF的APIView
    """
    extra_permission_classes = ()
    # 仅当GET方法时会触发该权限的校验
    GET_permission_classes = ()

    # 仅当POST方法时会触发该权限的校验
    POST_permission_classes = ()

    # 仅当DELETE方法时会触发该权限的校验
    DELETE_permission_classes = ()

    # 仅当PUT方法时会触发该权限的校验
    PUT_permission_classes = ()

    view_logger_classes = ()

    def initial(self, request: Request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.check_extra_permissions(request)
        self.check_method_extra_permissions(request)

    def get_view_loggers(self, request: Request, *args, **kwargs):
        logger_classes = self.view_logger_classes or []
        if not logger_classes:
            return []
        view_loggers = [logger_class(view=self, request=request, *args, **kwargs) for logger_class in logger_classes]
        return view_loggers

    def handle_logging(self, request: Request, *args, **kwargs):
        view_loggers = self.get_view_loggers(request, *args, **kwargs)
        method = request.method.lower()
        for view_logger in view_loggers:
            view_logger.handle(request, *args, **kwargs)
            logger_fun = getattr(view_logger, f'handle_{method}', None)
            if logger_fun and isinstance(logger_fun, (FunctionType, MethodType)):
                logger_fun(request, *args, **kwargs)

    def get_extra_permissions(self):
        return [permission() for permission in self.extra_permission_classes]

    def check_extra_permissions(self, request: Request):
        for permission in self.get_extra_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )

    def get_method_extra_permissions(self):
        _name = self.request.method.upper()
        method_extra_permission_classes = getattr(self, f"{_name}_permission_classes", None)
        if not method_extra_permission_classes:
            return []
        return [permission() for permission in method_extra_permission_classes]

    def check_method_extra_permissions(self, request):
        for permission in self.get_method_extra_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )


class BatchModelApIView(CustomAPIView):
    """
    模型批量CRUD通用视图
    """
    model = None
    serializer_class = None
    POST_serializer_class = None
    PUT_serializer_class = None
    field_name = 'instanceId'
    instanceId_list_param_name = 'instanceIdList'
    instance_info_param_name = 'info'

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None
        serializer_class = getattr(self, f"{self.request.method}_serializer_class", None) or getattr(self,
                                                                                                     'serializer_class')
        serializer = serializer_class(*args, **kwargs)
        if isinstance(serializer, CustomModelSerializer):
            serializer.request = self.request
        return serializer

    def get(self, request: Request = None, *args, **kwargs):
        data = self.get_serializer(self.model.objects.filter(**{f'{self.field_name}__in': request.data}),
                                   many=True).data
        return SuccessResponse(data=data)

    def post(self, request: Request = None, *args, **kwargs):
        data = []
        for info in request.data:
            serializer = self.get_serializer(data=info)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data.append(serializer.data)
        return SuccessResponse(data=data)

    def put(self, request: Request = None, *args, **kwargs):
        data = []
        instanceId_list = request.data.get(self.instanceId_list_param_name, [])
        info = request.data.get(self.instance_info_param_name, {})
        for instanceId in instanceId_list:
            serializer = self.get_serializer(
                instance=self.model.objects.get(**{f'{self.field_name}': instanceId}),
                data=info,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return SuccessResponse(data=instanceId_list)

    def delete(self, request: Request = None, *args, **kwargs):
        self.model.objects.filter(**{f'{self.field_name}__in': request.data}).delete()
        return SuccessResponse(data=request.data)


class ModelRelationshipAPIView(CustomAPIView):
    """
    模型关联关系通用CRUD视图
    """
    model = None
    through_model = None
    relationship_model = None

    relationship_serializer = None
    field_name: str = None
    from_field_name: str = 'instanceId'
    to_field_name: str = None
    relationship_field_values = ()

    view_logger_classes = [CustomerRelationshipViewLogger, ]

    def get_relationship_data(self, instanceId: str):
        relationship_model_field_name = self.relationship_field_values[0]
        params = {}
        params[self.field_name] = instanceId
        business_key_dict = self.through_model.objects.filter(**params).values(
            *self.relationship_field_values).distinct()
        business_key_list = [ele[relationship_model_field_name] for ele in business_key_dict]

        params = {}
        params[f"{self.to_field_name}__in"] = business_key_list
        queryset = self.relationship_model.objects.filter(**params)

        data = ModelRelateUtils.model_to_dict(queryset, self.relationship_serializer, default=[])
        if 'creator' in self.relationship_field_values and 'ctime' in self.relationship_field_values:
            for _index in range(len(data)):
                ele = data[_index]
                ele['relationship_creator'] = business_key_dict[_index]['creator']
                ele['relationship_ctime'] = business_key_dict[_index]['ctime']
        return data

    def execute_method(self, execute: str, request: Request, instanceId: str, *args, **kwargs):
        method = request.method.lower()
        fun = None
        if execute == 'before':
            fun = getattr(self, f'before_{method}', None)
        elif execute == 'handle':
            fun = getattr(self, f'handle_{method}', None)
        elif execute == 'after':
            fun = getattr(self, f'after_{method}', None)
        if fun and isinstance(fun, (FunctionType, MethodType)):
            fun(request, instanceId, *args, **kwargs)

    def do_request(self, request: Request, instanceId: str, *args, **kwargs):
        self.execute_method('before', request, instanceId, *args, **kwargs)
        self.execute_method('handle', request, instanceId, *args, **kwargs)
        self.execute_method('after', request, instanceId, *args, **kwargs)
        self.handle_logging(request, instanceId=instanceId, *args, **kwargs)
        data = self.get_relationship_data(instanceId)
        return SuccessResponse(data)

    def get(self, request: Request, instanceId: str, *args, **kwargs):
        return self.do_request(request, instanceId, *args, **kwargs)

    def post(self, request: Request, instanceId: str, *args, **kwargs):
        return self.do_request(request, instanceId, *args, **kwargs)

    def put(self, request: Request, instanceId: str, *args, **kwargs):
        return self.do_request(request, instanceId, *args, **kwargs)

    def delete(self, request: Request, instanceId: str, *args, **kwargs):
        return self.do_request(request, instanceId, *args, **kwargs)


class ModelRelationshipView(ModelRelationshipAPIView):
    """
    模型关联关系通用CRUD视图
    """

    def handle_get(self, request: Request, instanceId: str, *args, **kwargs):
        data = self.get_relationship_data(instanceId)
        return SuccessResponse(data)

    def handle_post(self, request: Request, instanceId: str, *args, **kwargs):
        relationship_model_field_name = self.relationship_field_values[0]
        params = {}
        params[f"{self.to_field_name}__in"] = request.data
        queryset = self.relationship_model.objects.filter(**params)

        exist_list = [getattr(ele, self.to_field_name) for ele in queryset]
        bulk_info = []
        for _id in exist_list:
            info = {}
            info[relationship_model_field_name] = _id
            info[self.field_name] = instanceId
            info['creator'] = request.user.username
            bulk_info.append(self.through_model(**info))
        self.through_model.objects.bulk_create(bulk_info)
        data = self.get_relationship_data(instanceId)
        return SuccessResponse(data)

    def handle_put(self, request: Request, instanceId: str, *args, **kwargs):
        relationship_model_field_name = self.relationship_field_values[0]

        params1 = {}
        params1[f"{self.field_name}"] = instanceId
        params2 = {}
        params2[f"{relationship_model_field_name}__in"] = request.data

        relationships = self.through_model.objects.filter(**params1).exclude(**params2)
        relationships.delete()

        params = {}
        params[f"{self.field_name}"] = instanceId

        instanceId_dict = self.through_model.objects.filter(**params).values(*self.relationship_field_values).distinct()
        instanceId_list = [ele.get(relationship_model_field_name) for ele in instanceId_dict]
        create_list = list(set(request.data).difference(set(instanceId_list)))
        for _id in create_list:
            info = {}
            info[relationship_model_field_name] = _id
            info[self.field_name] = instanceId
            info['creator'] = request.user.username
        data = self.get_relationship_data(instanceId)
        return SuccessResponse(data)

    def handle_delete(self, request: Request, instanceId: str, *args, **kwargs):
        relationship_model_field_name = self.relationship_field_values[0]
        params = {}
        params[f"{self.field_name}"] = instanceId
        params[f"{relationship_model_field_name}__in"] = request.data
        self.through_model.objects.filter(**params).delete()
        data = self.get_relationship_data(instanceId)
        return SuccessResponse(data)
