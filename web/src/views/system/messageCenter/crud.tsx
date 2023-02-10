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
            }
        },
    }
}
