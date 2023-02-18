import * as api from "./api";
import {dict, compute, PageQuery, AddReq, DelReq, EditReq, CrudExpose, CrudOptions,} from "@fast-crud/fast-crud";
import {request} from "/@/utils/service";
import {dictionary} from "/@/utils/dictionary";
import tableSelector from "/@/components/tableSelector/index.vue"
import {shallowRef} from "vue";

interface CreateCrudOptionsTypes {
    crudOptions: CrudOptions;
}

export const createCrudOptions = function ({crudExpose}: { crudExpose: CrudExpose }): CreateCrudOptionsTypes {
    const pageRequest = async (query: PageQuery) => {
        return await api.GetList(query);
    };
    const editRequest = async ({form, row}: EditReq) => {
        form.id = row.id;
        return await api.UpdateObj(form);
    };
    const delRequest = async ({row}: DelReq) => {
        return await api.DelObj(row.id);
    };
    const addRequest = async ({form}: AddReq) => {
        return await api.AddObj(form);
    };
    return {
        crudOptions: {
            request: {
                pageRequest,
                addRequest,
                editRequest,
                delRequest
            },
            columns: {

                id: {
                    title: 'id',
                    form: {
                        show: false
                    }

                },
                title: {
                    title: '标题',
                    search: {
                        disabled: false
                    },
                    type: ["text", "colspan"],
                    form: {
                        rules: [ // 表单校验规则
                            {
                                required: true,
                                message: '必填项'
                            }
                        ],
                        component: {span: 24, placeholder: '请输入标题'}
                    }
                },
                is_read: {
                    title: '是否已读',
                    type: 'dict-select',
                    column: {
                        show: false
                    },
                    dict: dict({
                        data: [
                            {label: '已读', value: true, color: 'success'},
                            {label: '未读', value: false, color: 'danger'}
                        ]
                    }),
                    form: {
                        show: false
                    }
                },
                target_type: {
                    title: '目标类型',
                    type: ['dict-radio', 'colspan'],
                    width: 120,
                    // show() {
                    //     return vm.tabActivted === 'send'
                    // },
                    dict: dict({
                        data: [{value: 0, label: '按用户'}, {value: 1, label: '按角色'}, {
                            value: 2,
                            label: '按部门'
                        }, {value: 3, label: '通知公告'}]
                    }),
                    form: {
                        component: {
                            optionName: "el-radio-button"
                        },
                        rules: [
                            {
                                required: true,
                                message: '必选项',
                                trigger: ['blur', 'change']
                            }
                        ]
                    }
                },
                target_user: {
                    title: '目标用户',
                    search: {
                        disabled: true
                    },
                    width: 130,
                    disabled: true,
                    form: {
                        component: {
                            name: shallowRef(tableSelector),
                            vModel: "modelValue",
                            tableConfig: {
                                url: '/api/system/user/',
                                label: 'name',
                                value: 'id',
                                isMultiple: true,
                                columns: [{
                                    prop: 'name',
                                    label: '用户名称',
                                    width: 120
                                }, {
                                    prop: 'phone',
                                    label: '用户电话',
                                    width: 120
                                }]
                            }
                        },
                        show: compute(({form}) => {
                            return form.target_type === 0
                        }),
                        rules: [ // 表单校验规则
                            {
                                required: true,
                                message: '必填项'
                            }
                        ],

                    },
                    component: {
                        name: 'manyToMany',
                        valueBinding: 'user_info',
                        children: 'name'
                    }
                },
                target_role: {
                    title: '目标角色',
                    search: {
                        disabled: true
                    },
                    disabled: true,
                    width: 130,
                    form: {
                        component: {
                            name: shallowRef(tableSelector),
                            vModel: "modelValue",
                            tableConfig: {
                                url: '/api/system/role/',
                                label: 'name',
                                value: 'id',
                                isMultiple: true,
                                columns: [{
                                    prop: 'name',
                                    label: '角色名称'
                                },
                                    {
                                        prop: 'key',
                                        label: '权限标识'
                                    }]
                            }
                        },
                        show: compute(({form}) => {
                            return form.target_type === 1
                        }),
                        rules: [ // 表单校验规则
                            {
                                required: true,
                                message: '必填项'
                            }
                        ]
                    },
                    component: {
                        name: 'manyToMany',
                        valueBinding: 'role_info',
                        children: 'name'
                    }
                },
                target_dept: {
                    title: '目标部门',
                    search: {
                        disabled: true
                    },
                    width: 130,
                    type: 'table-selector',
                    form: {
                        component: {
                            name: shallowRef(tableSelector),
                            vModel: "modelValue",
                            tableConfig: {
                                url: '/api/system/dept/all_dept/',
                                label: 'name',
                                value: 'id',
                                isTree: true,
                                isMultiple: true,
                                columns: [{
                                    prop: 'name',
                                    label: '部门名称'
                                },
                                {
                                    prop: 'status_label',
                                    label: '状态'
                                },
                                {
                                    prop: 'parent_name',
                                    label: '父级部门'
                                }]
                            }
                        },
                        show: compute(({form}) => {
                            return form.target_type === 2
                        }),
                        rules: [ // 表单校验规则
                            {
                                required: true,
                                message: '必填项'
                            }
                        ],
                        itemProps: {
                            class: {yxtInput: true}
                        }
                    },
                    component: {
                        name: 'manyToMany',
                        valueBinding: 'dept_info',
                        children: 'name'
                    }
                },
                content: {
                    title: '内容',
                    column: {
                        width: 300,
                        show: false
                    },
                    type: ["editor-wang5", "colspan"],
                    form: {
                        rules: [ // 表单校验规则
                            {
                                required: true,
                                message: '必填项'
                            }
                        ],
                        component: {
                            disabled: compute(({form}) => {
                                return form.disabled;
                            }),
                            id: "1", // 当同一个页面有多个editor时，需要配置不同的id
                            config: {},
                            uploader: {
                                type: "form",
                                buildUrl(res: any) {
                                    return res.url;
                                }
                            }
                        }
                    }
                }
            }
        },
    }
}
