<template>
	<div class="permission-com">
		<el-button type="primary" class="pc-save-btn">保存菜单授权</el-button>

		<el-collapse v-model="collapseCurrent" @change="handleCollapseChange" accordion>
			<el-collapse-item v-for="item in menuData" :key="item.key" :name="item.key">
				<template #title>
					<div @click.stop="null">
						<p class="pc-collapse-title">
							<el-checkbox v-model="item.isCheck">
								<span>{{ item.name }}</span>
							</el-checkbox>
						</p>
						<div v-show="!collapseCurrent.includes(item.key)">
							<el-checkbox v-for="btn in item.btns" :key="btn.value" :label="btn.value" v-model="btn.isCheck">{{ btn.label }}</el-checkbox>
						</div>
					</div>
				</template>
				<div class="pc-collapse-main">
					<div class="pccm-item">
						<p>允许对这些数据有以下操作</p>
						<el-checkbox v-for="btn in item.btns" :key="btn.value" v-model="btn.isCheck" :label="btn.value">
							<p class="btn-item">
								{{ btn.role ? `${btn.label}(${btn.role})` : btn.label }}
								<span @click.stop.prevent="handleSettingClick(item, btn.value)">
									<el-icon><Setting /></el-icon>
								</span>
							</p>
						</el-checkbox>
					</div>

					<div class="pccm-item">
						<p>对这些数据有以下字段权限</p>

						<el-radio-group v-model="item.radio">
							<el-radio label="1">全部字段可查看可编辑</el-radio>
							<el-radio label="2">全部字段仅可查看不可编辑</el-radio>
							<el-radio label="3">自定义字段权限</el-radio>
						</el-radio-group>

						<ul v-show="item.radio === '3'" class="columns-list">
							<li class="columns-head">
								<div class="width-txt">
									<span>字段</span>
								</div>

								<div v-for="btn in item.btns" :key="btn.value" class="width-check">
									<el-checkbox :label="btn.value" @change="handleColumnChange($event, item, btn.value)">
										<span>{{ btn.label }}</span>
									</el-checkbox>
								</div>
							</li>

							<li v-for="(c_item, c_index) in item.columns" :key="c_index" class="columns-item">
								<div class="width-txt">{{ c_item.name }}</div>
								<div v-for="btn in item.btns" :key="btn.value" class="width-check">
									<el-checkbox v-model="c_item[btn.value]" class="ci-checkout"></el-checkbox>
								</div>
							</li>
						</ul>
					</div>
				</div>
			</el-collapse-item>
		</el-collapse>

		<el-dialog v-model="dialogVisible" title="数据权限配置" width="400px" :close-on-click-modal="false" :before-close="handleDialogClose">
			<div class="pc-dialog">
				<el-select v-model="dataPermission" @change="handlePermissionRangeChange" class="dialog-select" placeholder="请选择">
					<el-option v-for="item in dataPermissionRange" :key="item.value" :label="item.label" :value="item.value" />
				</el-select>

				<el-tree-select
					v-if="dataPermission === 4"
					node-key="id"
					v-model="customDataPermission"
					:props="defaultTreeProps"
					:data="deptData"
					multiple
					check-strictly
					:render-after-expand="false"
					show-checkbox
					class="dialog-tree"
				/>
			</div>
			<template #footer>
				<div>
					<el-button type="primary" @click="handleDialogConfirm"> 确定 </el-button>
					<el-button @click="handleDialogClose"> 取消 </el-button>
				</div>
			</template>
		</el-dialog>
	</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import XEUtils from 'xe-utils';
import { errorNotification } from '/@/utils/message';
import { getDataPermissionRange, getDataPermissionDept } from './api';
import { MenuDataType, DataPermissionRangeType, CustomDataPermissionDeptType } from './types';

const defaultTreeProps = {
	children: 'children',
	label: 'name',
	value: 'id',
};

let menuData = ref<MenuDataType[]>([
	{
		key: '1',
		name: '用户管理',
		isCheck: true,
		radio: '1',
		btns: [
			{ label: '新增', value: 'create', isCheck: true, role: '' },
			{ label: '编辑', value: 'edit', isCheck: true, role: '' },
			{ label: '查询', value: 'look', isCheck: true, role: '' },
		],
		columns: [
			{ name: '姓名', create: true, edit: true, delete: true, look: true },
			{ name: '性别', create: false, edit: true, delete: false, look: true },
			{ name: '地址', create: true, edit: false, delete: true, look: false },
		],
	},
	{
		key: '2',
		name: '系统管理',
		isCheck: false,
		radio: '2',
		btns: [
			{ label: '新增', value: 'create', isCheck: false, role: '' },
			{ label: '编辑', value: 'edit', isCheck: true, role: '' },
			{ label: '删除', value: 'delete', isCheck: false, role: '' },
			{ label: '查询', value: 'look', isCheck: true, role: '' },
		],
		columns: [
			{ name: '姓名', create: false, edit: true, delete: false, look: true },
			{ name: '性别', create: true, edit: true, delete: true, look: true },
			{ name: '地址', create: true, edit: false, delete: true, look: false },
		],
	},
]);
let collapseCurrent = ref(['1']);
let menuCurrent = ref<Partial<MenuDataType>>({});
let menuBtnCurrent = ref('');
let dialogVisible = ref(false);
let dataPermissionRange = ref<DataPermissionRangeType[]>([]);
let deptData = ref<CustomDataPermissionDeptType[]>([]);
let dataPermission = ref();
let customDataPermission = ref([]);

const fetchData = async () => {
	try {
		const resRange = await getDataPermissionRange();
		if (resRange?.code === 2000) {
			dataPermissionRange.value = resRange.data;
		}
	} catch {
		return;
	}
};

const handleCollapseChange = (val: string) => {
	collapseCurrent.value = [val];
};

const handleSettingClick = (record: MenuDataType, btnType: string) => {
	menuCurrent.value = record;
	menuBtnCurrent.value = btnType;
	dialogVisible.value = true;
};

const handleColumnChange = (val: boolean, record: MenuDataType, btnType: string) => {
	for (const iterator of record.columns) {
		iterator[btnType] = val;
	}
};

const handlePermissionRangeChange = async (val: number) => {
	if (val === 4) {
		const res = await getDataPermissionDept();
		const data = XEUtils.toArrayTree(res.data, { parentKey: 'parent', strict: false });
		deptData.value = data;
	}
};

const handleDialogConfirm = () => {
	if (dataPermission.value !== 0 && !dataPermission.value) {
		errorNotification('请选择');
		return;
	}

	//if (dataPermission.value !== 4) {}
	for (const iterator of menuData.value) {
		if (iterator.key === menuCurrent.value.key) {
			for (const b of iterator.btns) {
				if (b.value === menuBtnCurrent.value) {
					const findItem = dataPermissionRange.value.find((i) => i.value === dataPermission.value);
					b.role = findItem?.label || '';
				}
			}
		}
	}
	handleDialogClose();
};
const handleDialogClose = () => {
	dialogVisible.value = false;
	customDataPermission.value = [];
	dataPermission.value = null;
};

onMounted(() => {
	fetchData();
});
</script>

<style lang="scss" scoped>
.permission-com {
	margin: 15px;
	box-sizing: border-box;
	.pc-save-btn {
		margin-bottom: 15px;
	}
	.pc-collapse-title {
		line-height: 32px;
		span {
			font-size: 16px;
		}
	}
	.pc-collapse-main {
		padding-top: 15px;
		box-sizing: border-box;
		.pccm-item {
			margin-bottom: 10px;

			.btn-item {
				display: flex;
				align-items: center;
				span {
					margin-left: 5px;
				}
			}
			.columns-list {
				.width-txt {
					width: 200px;
				}
				.width-check {
					width: 80px;
				}
				.width-icon {
					cursor: pointer;
				}
				.columns-head {
					display: flex;
					align-items: center;
					padding: 6px 0;
					border-bottom: 1px solid #ebeef5;
					box-sizing: border-box;
					span {
						font-weight: 900;
					}
				}
				.columns-item {
					display: flex;
					align-items: center;
					padding: 6px 0;
					box-sizing: border-box;
					.ci-checkout {
						height: auto !important;
					}
				}
			}
		}
	}

	.pc-dialog {
		.dialog-select {
			width: 100%;
		}
		.dialog-tree {
			width: 100%;
			margin-top: 20px;
		}
	}
}
</style>

<style lang="scss">
.permission-com {
	.el-collapse {
		border-top: none;
		border-bottom: none;
	}
	.el-collapse-item {
		margin-bottom: 15px;
	}
	.el-collapse-item__header {
		height: auto;
		padding: 15px;
		border-radius: 8px;
		border-top: 1px solid #ebeef5;
		border-left: 1px solid #ebeef5;
		border-right: 1px solid #ebeef5;
		box-sizing: border-box;
	}
	.el-collapse-item__header.is-active {
		border-radius: 8px 8px 0 0;
		background-color: #fafafa;
	}
	.el-collapse-item__wrap {
		padding: 15px;
		border-left: 1px solid #ebeef5;
		border-right: 1px solid #ebeef5;
		border-top: 1px solid #ebeef5;
		border-radius: 0 0 8px 8px;
		background-color: #fafafa;
		box-sizing: border-box;
		.el-collapse-item__content {
			padding-bottom: 0;
		}
	}
}
</style>
