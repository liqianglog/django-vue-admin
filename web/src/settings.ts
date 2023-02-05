// 引入fast-crud
import { FastCrud } from "@fast-crud/fast-crud";
import "@fast-crud/fast-crud/dist/style.css";
import { setLogger } from '@fast-crud/fast-crud'
// element
import ui from "@fast-crud/ui-element";
import { request } from "/@/utils/service.ts";

export default {
    async install(app: any, options: any) {
        // 先安装ui
        app.use(ui);
        // 然后安装FastCrud
        app.use(FastCrud, {
            //i18n, //i18n配置，可选，默认使用中文，具体用法请看demo里的 src/i18n/index.js 文件
            // 此处配置公共的dictRequest（字典请求）
            async dictRequest({ dict }: any) {
                return await request({ url: dict.url }); //根据dict的url，异步返回一个字典数组
            },
            //公共crud配置
            commonOptions() {
                return {
                    request: {
                        //接口请求配置
                        //你项目后台接口大概率与fast-crud所需要的返回结构不一致，所以需要配置此项
                        //请参考文档http://fast-crud.docmirror.cn/api/crud-options/request.html
                        transformQuery: ({ page, form, sort }: any) => {
                            //转换为你pageRequest所需要的请求参数结构
                            return { page, form, sort };
                        },
                        transformRes: ({ res }: any) => {
                            //将pageRequest的返回数据，转换为fast-crud所需要的格式
                            //return {records,currentPage,pageSize,total};
                            return { records: res.data, currentPage: res.page, pageSize: res.limit, total: res.total }
                        }
                    },
                };
            },
        });
        setLogger({ level: 'error' })
    }
}

