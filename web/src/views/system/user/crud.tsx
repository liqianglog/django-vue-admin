import * as api from "./api";
import { dict, PageQuery, AddReq, DelReq, EditReq, CrudExpose, CrudOptions, } from "@fast-crud/fast-crud";
import { request } from "/@/utils/service";
import { dictionary } from "/@/utils/dictionary";
interface CreateCrudOptionsTypes {
    crudOptions: CrudOptions;
}

export const createCrudOptions = function ({ crudExpose }: { crudExpose: CrudExpose }): CreateCrudOptionsTypes {
    const pageRequest = async (query: PageQuery) => {
        return await api.GetList(query);
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
                delRequest
            },
            rowHandle: {
                width: 400,
                buttons: {
                    orderExample: {
                        text: "重置密码",
                        click: () => {
                            console.log("reset password")
                        }
                    }
                },

            },
            columns: {
                _index: {
                    title: '序号',
                    form: { show: false },
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
                    column: {
                        show: false
                    },
                    search: {
                        show: true,
                        component: {
                            props: {
                                clearable: true
                            },
                            placeholder: '请输入关键词'
                        }
                    },
                    form: {
                        show: false,
                        component: {
                            props: {
                                clearable: true
                            }
                        }
                    },
                },
                username: {
                    title: '账号',
                    search: {
                        show: true,
                    },
                    minWidth: 100,
                    type: 'input',
                    form: {
                        rules: [ // 表单校验规则
                            {
                                required: true,
                                message: '账号必填项'
                            }
                        ],
                        component: {
                            placeholder: '请输入账号'
                        },
                    }
                },
                password: {
                    title: '密码',
                    type: 'input',
                    column: {
                        show: false
                    },
                    editForm: {
                        show: false
                    },
                    form: {
                        rules: [ // 表单校验规则
                            {
                                required: true,
                                message: '密码必填项'
                            }
                        ],
                        component: {
                            span: 12,
                            showPassword: true,
                            placeholder: '请输入密码'
                        },
                        // value: vm.systemConfig('base.default_password'),
                    },
                    /* valueResolve(row, key) {
                        if (row.password) {
                            row.password = vm.$md5(row.password)
                        }
                    } */
                },
                name: {
                    title: '姓名',
                    search: {
                        show: true,
                    },
                    type: 'input',
                    form: {
                        rules: [ // 表单校验规则
                            {
                                required: true,
                                message: '姓名必填项'
                            }
                        ],
                        component: {
                            span: 12,
                            placeholder: '请输入姓名'
                        },
                    }
                },
                dept: {
                    title: '部门',
                    search: {
                        disabled: true
                    },
                    type: 'dict-tree',
                    dict: dict({
                        isTree: true,
                        url: '/api/system/dept/all_dept/',
                        value: 'id',
                        label: 'name',
                        getData: async ({ url }: { url: string }) => {
                            return request({
                                url: url,
                            }).then((ret: any) => {
                                return ret.data
                            })
                        }
                    }),
                    form: {
                        component: {
                            filterable: true,
                            placeholder: '请选择角色',
                            props: {
                                props: {
                                    value: "id",
                                    label: "name",
                                }
                            }
                        },
                    },
                },
                role: {
                    title: '角色',
                    search: {
                        disabled: true
                    },
                    type: 'dict-tree',
                    dict: dict({
                        url: '/api/system/role/',
                        value: 'id',
                        label: 'name',
                        isTree: true,
                        getData: async ({ url }: { url: string }) => {
                            return request({
                                url: url,
                                params: {
                                    page: 1,
                                    limit: 10
                                }
                            }).then((ret: any) => {
                                return ret.data
                            })
                        }
                    }),
                    form: {
                        component: {
                            filterable: true,
                            placeholder: '请选择角色',
                            props: {
                                props: {
                                    value: "id",
                                    label: "name",
                                }
                            }
                        },
                    }
                },
                mobile: {
                    title: '手机号码',
                    search: {
                        show: true,
                    },
                    type: 'input',
                    form: {
                        rules: [
                            {
                                max: 20,
                                message: '请输入正确的手机号码',
                                trigger: 'blur'
                            },
                            {
                                pattern: /^1[3-9]\d{9}$/,
                                message: '请输入正确的手机号码'
                            }
                        ],
                        component: {
                            placeholder: '请输入手机号码'
                        }
                    }
                },
                email: {
                    title: '邮箱',
                    form: {
                        rules: [
                            {
                                type: 'email',
                                message: '请输入正确的邮箱地址',
                                trigger: ['blur', 'change']
                            }
                        ],
                        component: {
                            placeholder: '请输入邮箱'
                        }
                    }
                },
                gender: {
                    title: '性别',
                    type: 'dict-radio',
                    dict: dict({
                        data: dictionary('gender')
                    }),
                    form: {
                        value: 1,
                        component: {
                            span: 12
                        }
                    },
                    component: { props: { color: 'auto' } } // 自动染色
                },
                user_type: {
                    title: '用户类型',
                    search: {
                        show: true,
                    },
                    type: 'dict-select',
                    dict: dict({
                        data: dictionary('user_type')
                    }),
                    form: {
                        show: false,
                        value: 0,
                        component: {
                            span: 12
                        }
                    }
                },
                is_active: {
                    title: '状态',
                    search: {
                        show: true,
                    },
                    type: 'dict-radio',
                    dict: dict({
                        data: dictionary('button_status_bool')
                    }),
                    form: {
                        value: true,
                        component: {
                            span: 12
                        }
                    }
                },
                avatar: {
                    title: '头像',
                    type: 'avatar-cropper',
                    form: {
                        component: {
                            props: {
                                elProps: { // 与el-uploader 配置一致
                                    multiple: false,
                                    limit: 1 // 限制5个文件
                                },
                                sizeLimit: 500 * 1024 // 不能超过限制
                            },
                            span: 24
                        },
                        helper: '限制文件大小不能超过500k'
                    }
                }
            }
        }
    };
}