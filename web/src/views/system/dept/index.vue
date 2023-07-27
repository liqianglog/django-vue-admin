<template>
	<fs-page>
		<el-row class="dept-el-row">
			<el-col :span="6">
				<div class="dept-box dept-left">
					<TreeCom :treeData="treeData" @setFormInitData="setFormInitData" @updateDept="handleUpdateMenu"
						@deleteDept="handleDeleteMenu" />
				</div>
			</el-col>

			<el-col :span="18">
				<div class="dept-box dept-form">
					<el-form ref="formRef" :rules="rules" :model="deptFormData" label-width="120px" label-position="right">
						<el-divider>
							<strong>部门配置</strong>
						</el-divider>
						<el-row>
							<el-col :span="10">
								<el-form-item label="部门ID" prop="id">
									<el-input v-model="deptFormData.id" disabled />
								</el-form-item>
							</el-col>
							<el-col :span="10">
								<el-form-item label="父级部门ID" prop="parent">
									<el-input v-model="deptFormData.parent" />
								</el-form-item>
							</el-col>
							<el-col :span="10">
								<el-form-item required label="部门名称" prop="name">
									<el-input v-model="deptFormData.name" />
								</el-form-item>
							</el-col>
							<el-col :span="10">
								<el-form-item required label="部门标识" prop="key">
									<el-input v-model="deptFormData.key" />
								</el-form-item>
							</el-col>
							<el-col :span="10">
								<el-form-item label="负责人" prop="owner">
									<el-input v-model="deptFormData.owner" />
								</el-form-item>
							</el-col>
							<el-col :span="10">
								<el-form-item label="联系电话" prop="phone">
									<el-input v-model="deptFormData.phone" />
								</el-form-item>
							</el-col>
							<el-col :span="10">
								<el-form-item label="邮箱" prop="email">
									<el-input v-model="deptFormData.email" />
								</el-form-item>
							</el-col>
							<el-col :span="10">
								<el-form-item label="排序" prop="sort">
									<el-input-number v-model="deptFormData.sort" controls-position="right" />
								</el-form-item>
							</el-col>

							<el-col class="center">
								<el-divider>
									<el-button @click="handleUpdateMenu('update')" type="primary" round
										:disabled="!deptFormData.id || deptBtnLoading">保存</el-button>
									<el-button @click="handleUpdateMenu('create')" type="primary" round :disabled="deptBtnLoading">新建
									</el-button>
									<el-button @click="handleDeleteMenu" type="primary" round>删除部门
									</el-button>
								</el-divider>
							</el-col>
						</el-row>
					</el-form>
				</div>
			</el-col>
		</el-row>

		<el-drawer v-model="drawerVisible" title="部门配置" direction="rtl" size="500px" :close-on-click-modal="false"
			:before-close="handleDrawerClose">
			<FormCom v-if="drawerVisible" :initFormData="drawerFormData" @drawerClose="handleDrawerClose" />
		</el-drawer>
	</fs-page>
</template>

<script lang="ts" setup name="dept">
import { ref, onMounted, reactive } from 'vue';
import XEUtils from 'xe-utils';
import { ElForm, ElMessageBox, FormRules } from 'element-plus';
import TreeCom from './components/TreeCom.vue'
import FormCom from './components/FormCom.vue'
import { GetList, AddObj, UpdateObj, DelObj } from './api';
import { successMessage } from '../../../utils/message';
import { APIResponseData, DeptFormDataType, TreeItemType } from './types';

let treeData = ref([]);
let deptFormData = reactive<DeptFormDataType>({
	id: '',
	key: '',
	parent: '',
	name: '',
	owner: '',
	phone: '',
	email: '',
	sort: 0,
	is_catalog: true,
})
let deptBtnLoading = ref(false)
let drawerVisible = ref(false)
let drawerFormData = ref<Partial<TreeItemType>>({})
const formRef = ref<InstanceType<typeof ElForm>>();

const rules = reactive<FormRules>({
	name: [{ required: true, message: '部门名称必填', trigger: 'blur' }],
	key: [{ required: true, message: '部门标识必填', trigger: 'blur' }],
});

const getData = async () => {
	let res: APIResponseData = await GetList({});

	if (res?.code === 2000 && Array.isArray(res.data)) {
		const result = XEUtils.toArrayTree(res.data, {
			parentKey: 'parent',
			children: 'children',
			strict: true,
		});

		treeData.value = result;
	}
};

const setFormInitData = (data: DeptFormDataType) => {
	deptFormData.id = data.id;
	deptFormData.key = data.key;
	deptFormData.name = data.name;
	deptFormData.parent = data.parent;
	deptFormData.owner = data.owner;
	deptFormData.phone = data.phone;
	deptFormData.email = data.email;
	deptFormData.sort = data.sort;
};

const handleDeleteMenu = (id: string, callback: Function) => {
	ElMessageBox.confirm(
		'您确认删除该部门吗?',
		'温馨提示',
		{
			confirmButtonText: '确认',
			cancelButtonText: '取消',
			type: 'warning',
		}
	).then(async () => {
		const res: APIResponseData = await DelObj(id)
		callback()
		if (res?.code === 2000) {
			successMessage(res.msg as string);
			getData();
		}
	})
};

const handleUpdateMenu = (type: string, record?: TreeItemType) => {
	if (type === 'update' && record) {
		drawerFormData.value = record
	}
	drawerVisible.value = true
	//form.component == '' ? (form.is_catalog = true) : (form.is_catalog = false);
	/* formRef.value?.validate(async (valid) => {
		if (!valid) return
		try {
			let res;
			deptBtnLoading.value = true
			if (type === 'update') {
				res = await UpdateObj(deptFormData);
			} else if (type === 'create') {
				res = await AddObj(deptFormData)
			}
			if (res?.code === 2000) {
				successMessage(res.msg as string);
				getData();
			}
		} finally {
			type === 'create' && formRef.value?.resetFields();
			deptBtnLoading.value = false
		}
	}); */

};
const handleDrawerClose = () => {
	drawerVisible.value = false
	drawerFormData.value = {}
}

onMounted(() => {
	getData();
});
</script>

<style lang="scss" scoped>
.dept-el-row {
	height: 100%;
	overflow: hidden;

	.el-col {
		height: 100%;
		padding: 10px 0;
		box-sizing: border-box;
	}
}

.dept-box {
	height: 100%;
	padding: 10px;
	background-color: #fff;
	box-sizing: border-box;
}

.dept-left {
	position: relative;
	border-radius: 0 8px 8px 0;

	.dl-nav {
		margin-bottom: 10px;
	}
}

.dept-form {
	border-radius: 8px 0 0 8px;
	margin-left: 10px;
}

.font-normal {
	font-family: Helvetica Neue, Helvetica, PingFang SC, Hiragino Sans GB, Microsoft YaHei, SimSun, sans-serif;
}
</style>