// 引入fast-crud
import { FastCrud, useTypes } from '@fast-crud/fast-crud';
const { getType } = useTypes();
import '@fast-crud/fast-crud/dist/style.css';
import { setLogger } from '@fast-crud/fast-crud';
// element
import ui from '@fast-crud/ui-element';
import { request } from '/@/utils/service';
//扩展包
import { FsExtendsEditor } from '@fast-crud/fast-extends';
import '@fast-crud/fast-extends/dist/style.css';
export default {
	async install(app: any, options: any) {
		// 先安装ui
		app.use(ui);
		// 然后安装FastCrud
		app.use(FastCrud, {
			//i18n, //i18n配置，可选，默认使用中文，具体用法请看demo里的 src/i18n/index.js 文件
			// 此处配置公共的dictRequest（字典请求）
			async dictRequest({ dict }: any) {
				return await request({ url: dict.url, params: dict.params || {} }); //根据dict的url，异步返回一个字典数组
			},
			//公共crud配置
			commonOptions() {
				return {
					request: {
						//接口请求配置
						//你项目后台接口大概率与fast-crud所需要的返回结构不一致，所以需要配置此项
						//请参考文档http://fast-crud.docmirror.cn/api/crud-options/request.html
						transformQuery: ({ page, form, sort }: any) => {
							if (sort.asc !== undefined) {
								form['ordering'] = `${sort.asc ? '' : '-'}${sort.prop}`;
							}
							//转换为你pageRequest所需要的请求参数结构
							return { page: page.currentPage, limit: page.pageSize, ...form };
						},
						transformRes: ({ res }: any) => {
							//将pageRequest的返回数据，转换为fast-crud所需要的格式
							//return {records,currentPage,pageSize,total};
							return { records: res.data, currentPage: res.page, pageSize: res.limit, total: res.total };
						},
					},
					/* search: {
						layout: 'multi-line',
						collapse: true,
						col: {
							span: 4,
						},
						options: {
							labelCol: {
								style: {
									width: '100px',
								},
							},
						},
					}, */
				};
			},
		});
		//富文本
		app.use(FsExtendsEditor, {
			wangEditor: {
				width: 300,
			},
		});
		setLogger({ level: 'error' });
		// 设置自动染色
		const dictComponentList = ['dict-cascader', 'dict-checkbox', 'dict-radio', 'dict-select', 'dict-switch', 'dict-tree'];
		dictComponentList.forEach((val) => {
			getType(val).column.component.color = 'auto';
		});
	},
};
