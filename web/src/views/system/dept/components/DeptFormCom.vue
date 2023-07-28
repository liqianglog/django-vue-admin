<template>
	<el-form ref="formRef" :rules="rules" :model="deptFormData" label-width="100px" label-position="right" class="dept-form-com">
		<el-form-item label="父级部门" prop="parent">
			<el-select v-model="deptFormData.parent" style="width: 100%">
				<el-option v-for="item in deptAllList" :key="item.id" :label="item.name" :value="item.id" />
			</el-select>
		</el-form-item>
		<el-form-item required label="部门名称" prop="name">
			<el-input v-model="deptFormData.name" />
		</el-form-item>
		<el-form-item required label="部门标识" prop="key">
			<el-input v-model="deptFormData.key" />
		</el-form-item>
		<el-form-item label="负责人" prop="owner">
			<el-input v-model="deptFormData.owner" />
		</el-form-item>
		<el-form-item label="备注" prop="remark">
			<el-input v-model="deptFormData.remark" maxlength="200" show-word-limit type="textarea" />
		</el-form-item>
		<el-form-item>
			<el-button @click="handleUpdateMenu" type="primary" :disabled="deptBtnLoading">
				{{ deptFormData.id ? '保存' : '新增' }}
			</el-button>
			<el-button @click="handleClose">取消 </el-button>
		</el-form-item>
	</el-form>
</template>

<script lang="ts" setup>
import { reactive, ref, onMounted } from 'vue';
import { ElForm, FormRules } from 'element-plus';
import { getAllDeptList, AddObj, UpdateObj } from '../api';
import { successNotification } from '../../../../utils/message';
import { DeptFormDataType, TreeItemType, DeptListType } from '../types';

interface IProps {
	initFormData: TreeItemType | null;
}

const formRef = ref<InstanceType<typeof ElForm>>();
const rules = reactive<FormRules>({
	name: [{ required: true, message: '部门名称必填', trigger: 'blur' }],
	key: [{ required: true, message: '部门标识必填', trigger: 'blur' }],
});

const props = withDefaults(defineProps<IProps>(), {
	initFormData: () => null,
});
const emit = defineEmits(['drawerClose']);

let deptAllList = ref<DeptListType[]>([]);
let deptFormData = reactive<DeptFormDataType>({
	key: '',
	parent: '',
	name: '',
	owner: '',
	remark: '',
	is_catalog: true,
});
let deptBtnLoading = ref(false);

const getData = async () => {
	const res = await getAllDeptList();
	if (res?.code === 2000) {
		deptAllList.value = res.data;
	}
};

const setDeptFormData = () => {
	if (props.initFormData?.id) {
		deptFormData.id = props.initFormData?.id;
		deptFormData.key = props.initFormData.key || '';
		deptFormData.parent = props.initFormData.parent || '';
		deptFormData.name = props.initFormData.name || '';
		deptFormData.owner = props.initFormData.owner || '';
	}
};

const handleUpdateMenu = () => {
	formRef.value?.validate(async (valid) => {
		if (!valid) return;
		try {
			let res;
			deptBtnLoading.value = true;
			if (deptFormData.id) {
				res = await UpdateObj(deptFormData);
			} else {
				res = await AddObj(deptFormData);
			}
			if (res?.code === 2000) {
				successNotification(res.msg as string);
				handleClose('submit');
			}
		} finally {
			deptBtnLoading.value = false;
		}
	});
};

const handleClose = (type: string = '') => {
	emit('drawerClose', type);
	formRef.value?.resetFields();
};

onMounted(async () => {
	await getData();
	setDeptFormData();
});
</script>

<style lang="scss" scoped>
.dept-form-com {
	height: 100%;
	padding: 20px;
	box-sizing: border-box;
}
</style>
