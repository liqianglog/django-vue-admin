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

    /**
     * 懒加载
     * @param row
     * @returns {Promise<unknown>}
     */
    const loadContentMethod = (tree: any, treeNode: any, resolve: any) => {
        api.GetList({ parent: tree.id }).then((res: any) => {
            resolve(res.data);
        });
    };

    return {
        crudOptions: {
            request: {
                pageRequest,
                addRequest,
                editRequest,
                delRequest
            },
            pagination: {
                show: false,
            },
            table: {
                rowKey: 'id',
                lazy: true,
                load: loadContentMethod,
                treeProps: { children: 'children', hasChildren: 'hasChild' },
            },
            rowHandle:{
              fiexd:'right',
                width:310,
              buttons:{
                  addChildren:{
                      text: "添加子级",
                      type:"warning",
                      click(context){
                        const rowId =context.row.id
                         crudExpose.openAdd({ row: { parent: rowId } })
                      }
                  }
              }
            },
            columns: {
                _index: {
                    title: '序号',
                    form: { show: false },
                    column: {
                        type: 'index',
                        align: 'center',
                        width: '70px',
                        columnSetDisabled: true, //禁止在列设置中选择
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
                // parent: {
                //     column: {
                //         show: false
                //     },
                //     title: '上级部门',
                //     type: 'dict-tree',
                //     dict: dict({
                //         url: '/api/system/dept/all_dept/',
                //         value: 'id',
                //         label: 'name',
                //         isTree: true,
                //         getData: async ({ url }: { url: string }) => {
                //             return request({
                //                 url: url,
                //             }).then((ret: any) => {
                //                 return ret.data
                //             })
                //         }
                //     }),
                //     form: {
                //         helper: '默认留空为创建者的部门',
                //         component: {
                //             span: 12,
                //             props: {
                //                 props: {
                //                     value: "id",
                //                     label: "name",
                //                 }
                //             }
                //         }
                //     }
                // },
                name: {
                    title: '部门名称',
                    sortable: true,
                    treeNode: true, // 设置为树形列
                    search: {
                        disabled: false,
                        component: {
                            props: {
                                clearable: true
                            }
                        }
                    },
                    width: 180,
                    type: 'input',
                    form: {
                        rules: [
                            // 表单校验规则
                            { required: true, message: '部门名称必填项' }
                        ],
                        component: {
                            span: 12,
                            props: {
                                clearable: true
                            },
                            placeholder: '请输入部门名称'
                        },
                    }
                },
                key: {
                    title: '部门标识',
                    sortable: true,
                    form: {
                        component: {
                            props: {
                                clearable: true
                            },
                            placeholder: '请输入标识字符'
                        },
                    }
                },
                owner: {
                    title: '负责人',
                    sortable: true,
                    form: {
                        component: {
                            span: 12,
                            props: {
                                clearable: true
                            },
                            placeholder: '请输入负责人'
                        }
                    }
                },
                phone: {
                    title: '联系电话',
                    sortable: true,
                    form: {
                        component: {
                            span: 12,
                            props: {
                                clearable: true
                            },
                            placeholder: '请输入联系电话'
                        }
                    }
                },
                email: {
                    title: '邮箱',
                    sortable: true,
                    form: {
                        component: {
                            span: 12,
                            props: {
                                clearable: true
                            },
                            placeholder: '请输入邮箱'
                        },
                        rules: [
                            {
                                type: 'email',
                                message: '请输入正确的邮箱地址',
                                trigger: ['blur', 'change']
                            }
                        ]
                    }
                },
                sort: {
                    title: '排序',
                    sortable: true,
                    width: 80,
                    type: 'number',
                    form: {
                        value: 1,
                        component: {
                            span: 12,
                            placeholder: '请选择序号'
                        }
                    }
                },
                status: {
                    title: '状态',
                    sortable: true,
                    search: {
                        disabled: false
                    },
                    type: 'dict-radio',
                    dict: dict({
                        data: dictionary('button_status_bool')
                    }),
                    form: {
                        value: true,
                        component: {
                            span: 12,
                            placeholder: '请选择状态'
                        }
                    }
                }
            }
        },
    }
}
