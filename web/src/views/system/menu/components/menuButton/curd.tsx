import {CrudOptions, AddReq, DelReq, EditReq, dict, CrudExpose} from '@fast-crud/fast-crud';
import _ from 'lodash-es';
import * as api from "./api";
import { dictionary } from '/@/utils/dictionary';
interface CreateCrudOptionsTypes {
    crudOptions: CrudOptions;
}
import { request } from '/@/utils/service';
//此处为crudOptions配置
export const createCrudOptions = function ({crudExpose,selectOptions}: {crudExpose: CrudExpose,selectOptions:any}): CreateCrudOptionsTypes {

    const pageRequest = async (query: any) => {
        return await api.GetList({...query,menu:selectOptions.value.id});
    };
    const editRequest = async ({ form, row }: EditReq) => {
        form.id = row.id;
        return await api.UpdateObj(form);
    };
    const delRequest = async ({ row }: DelReq) => {
        return await api.DelObj(row.id);
    };
    const addRequest = async ({ form }: AddReq) => {
        return await api.AddObj(form);
    };
    return {
        crudOptions: {
            request: {
                pageRequest,
                addRequest,
                editRequest,
                delRequest,
            },
            form: {
                col: {span: 24},
                labelWidth: '100px',
                wrapper: {
                    is: 'el-dialog',
                    width: '600px',
                },
            },
            columns: {
                _index: {
                    title: '序号',
                    form: {show: false},
                    column: {
                        //type: 'index',
                        align: 'center',
                        width: '70px',
                        columnSetDisabled: true, //禁止在列设置中选择
                        formatter: (context) => {
                            //计算序号,你可以自定义计算规则，此处为翻页累加
                            let index = context.index ?? 1;
                            let pagination = crudExpose.crudBinding.value.pagination;
                            return ((pagination.currentPage ?? 1) - 1) * pagination.pageSize + index + 1;
                        },
                    },
                },
                search: {
                    title: '关键词',
                    column: {show: false},
                    type: 'text',
                    search: {show: true},
                    form: {
                        show: false,
                        component: {
                            placeholder: '输入关键词搜索',
                        },
                    },
                },
                id: {
                    title: 'ID',
                    type: 'text',
                    column: {show: false},
                    search: {show: false},
                    form: {show: false},
                },
                name: {
                    title: '权限名称',
                    type: 'dict-select',
                    search: {show: true},
                    dict:dict({
                        data:dictionary('system_button')
                    }),
                    column: {
                        minWidth: 120,
                        sortable: true,
                    },
                    form: {
                        rules: [{required: true, message: '角色名称必填'}],
                        component: {
                            placeholder: '输入角色名称搜索',
                        },
                    },
                },
                value: {
                    title: '权限值',
                    type: 'text',
                    search: {show: false},
                    column: {
                        width: 120,
                        sortable: true,
                    },
                    form: {
                        rules: [{required: true, message: '权限标识必填'}],
                        placeholder: '输入权限标识',
                    },
                },
                method: {
                    title: '请求方式',
                    search: {show: false},
                    type: 'dict-select',
                    column: {
                        width: 100,
                        sortable: true,
                    },
                    dict: dict({
                        data:[
                            { label: 'GET', value: 0 },
                            { label: 'POST', value: 1,color:'success' },
                            { label: 'PUT', value: 2 },
                            { label: 'DELETE', value: 3 ,color: 'danger'}
                        ]
                    })
                },
                api: {
                    title: '接口地址',
                    minWidth:200,
                    search: {show: false},
                    type: 'dict-select',
                    dict: dict({
                        getData(){
                            return request({ url: '/swagger.json' }).then((res:any) => {
                                const ret = Object.keys(res.paths)
                                const data = []
                                for (const item of ret) {
                                    const obj:any = {}
                                    obj.label = item
                                    obj.value = item
                                    data.push(obj)
                                }
                                return data
                            })
                        }
                    }),
                    column: {
                        width: 130,
                        sortable: true,
                    },
                    form: {
                        value: false,
                    },
                },
                status: {
                    title: '状态',
                    search: {show: true},
                    type: 'dict-radio',
                    dict: dict({
                        data: [
                            {
                                label: '启用',
                                value: true,
                                color: 'success',
                            },
                            {
                                label: '禁用',
                                value: false,
                                color: 'danger',
                            },
                        ],
                    }),
                    column: {
                        width: 90,
                        sortable: true,
                    },
                    form: {
                        value: true,
                    },
                },
                update_datetime: {
                    title: '更新时间',
                    type: 'text',
                    search: {show: false},
                    column: {
                        width: 170,
                        sortable: true,
                    },
                    form: {
                        show: false,
                        component: {
                            placeholder: '输入关键词搜索',
                        },
                    },
                },
                create_datetime: {
                    title: '创建时间',
                    type: 'text',
                    search: {show: false},
                    column: {
                        sortable: true,
                        width: 170,
                    },
                    form: {
                        show: false,
                        component: {
                            placeholder: '输入关键词搜索',
                        },
                    },
                },

                description: {
                    title: '备注',
                    type: 'textarea',
                    search: {show: false},
                    form: {
                        component: {
                            maxlength: 200,
                            placeholder: '输入备注',
                        },
                    },
                },
            },
        },
    };
};
