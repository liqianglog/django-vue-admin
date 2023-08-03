<template>
	<div class="permission-com">
		<div class="pc-item">
			<p class="pc-title">数据授权</p>
			<div class="pc-cell">
				<el-radio-group v-model="dataPermission" class="pc-data-permission">
					<el-radio v-for="item in dataPermissionRange" :key="item.label" :label="item.value" @change="handleChange">{{ item.label }}</el-radio>
				</el-radio-group>
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
					class="pc-custom-dept"
				/>
			</div>
		</div>

		<div class="pc-item pc-menu">
			<p class="pc-title">菜单授权</p>
			<div>
				<el-tree
					:props="defaultTreeProps"
					:data="menuData"
					show-checkbox
					node-key="id"
					default-expand-all
					:expand-on-click-node="false"
					class="dc-menu-tree"
				>
					<template #default="{ node, data }">
						<div class="pc-tree-node" :class="{ 'tree-node-label-border': !data.is_catalog }">
							<p class="tree-node-label">{{ node.label }}</p>
							<div v-if="!data.is_catalog">
								<ul class="menu-permission-list">
									<li v-for="m in data.menuPermission" :key="m.id" class="menu-permission-item">
										<el-checkbox v-model="m.id" :label="m.name" />
									</li>
								</ul>
								<ul class="menu-permission-list">
									<li v-for="m in data.columns" :key="m.id" class="menu-permission-item">
										<el-checkbox v-model="m.id" :label="m.title" />
									</li>
								</ul>
							</div>
						</div>
					</template>
				</el-tree>
			</div>
		</div>

		<div class="pc-btn">
			<el-button type="primary">确定</el-button>
			<el-button>取消</el-button>
		</div>
	</div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import XEUtils from 'xe-utils';
import { getDataPermissionRange, getDataPermissionDept, getDataPermissionMenu } from './api';
import { DataPermissionRangeType, CustomDataPermissionDeptType, CustomDataPermissionMenuType } from './types';

const defaultTreeProps = {
	children: 'children',
	label: 'name',
	value: 'id',
};

const data: any[] = [
	{
		id: 1,
		label: 'Level one 1',
		children: [
			{
				id: 4,
				label: 'Level two 1-1',
				isPenultimate: true,
				children: [
					{
						id: 9,
						label: 'Level three 1-1-1',
					},
					{
						id: 10,
						label: 'Level three 1-1-2',
					},
				],
			},
		],
	},
	{
		id: 2,
		label: 'Level one 2',
		isPenultimate: true,
		children: [
			{
				id: 5,
				label: 'Level two 2-1',
			},
			{
				id: 6,
				label: 'Level two 2-2',
			},
		],
	},
	{
		id: 3,
		label: 'Level one 3',
		isPenultimate: true,
		children: [
			{
				id: 7,
				label: 'Level two 3-1',
			},
			{
				id: 8,
				label: 'Level two 3-2',
			},
		],
	},
];

let dataPermission = ref();
let dataPermissionRange = ref<DataPermissionRangeType[]>([]);
let customDataPermission = ref();
let deptData = ref<CustomDataPermissionDeptType[]>([]);
let menuData = ref<CustomDataPermissionMenuType[]>([]);

const fetchData = async () => {
	try {
		const resRange = await getDataPermissionRange();
		const resMenu = await getDataPermissionMenu();

		if (resRange?.code === 2000) {
			dataPermissionRange.value = resRange.data;
		}
		if (resMenu?.code === 2000) {
			console.log(resMenu.data);
			menuData.value = resMenu.data;
		}
	} catch {
		return;
	}
};

const handleChange = async () => {
	if (dataPermission.value === 4) {
		const res = await getDataPermissionDept();
		const data = XEUtils.toArrayTree(res.data, { parentKey: 'parent', strict: false });
		deptData.value = data;
	}
};

const handleTestClick = (node: any, data: any) => {
	console.log(node, data);
};

onMounted(() => {
	fetchData();
});
</script>

<style lang="scss" scoped>
.permission-com {
	width: 100%;
	height: 100%;
	padding: 15px;
	box-sizing: border-box;
	.pc-item {
		width: 100%;
		margin-bottom: 15px;
		border-bottom: 1px #dcdfe6 solid;
	}
	.pc-title {
		font-weight: 600;
	}
	.pc-cell {
		display: flex;
		padding: 10px;
		overflow-x: auto;
		.pc-data-permission {
			min-width: 800px;
		}
		.pc-custom-dept {
			min-width: 200px;
		}
	}

	.pc-menu {
		height: calc(100% - 140px);
		overflow-y: auto;
	}

	.pc-tree-node {
		width: 100%;
		display: flex;
		align-items: center;

		.tree-node-label {
			font-size: 16px;
			margin-right: 20px;
		}
		.menu-permission-list {
			display: flex;
			align-items: center;
			.menu-permission-item {
				margin-right: 10px;
			}
		}
	}

	.tree-node-label-border {
		border-bottom: 1px #dcdfe6 solid;
	}

	.pc-btn {
		padding-bottom: 15px;
	}
}
</style>

<style lang="scss">
.dc-menu-tree {
	.el-tree-node__content {
		height: auto;
	}
}
</style>
