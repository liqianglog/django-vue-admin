<template>
	<div class="menu-form-com">
		<div class="menu-form-alert">
			1.红色菜单代表状态禁用;<br />
			2.添加菜单，如果是目录，组件地址为空即可;<br />
			3.添加根节点菜单，父级ID为空即可;<br />
			4.支持拖拽菜单;
		</div>
		<el-form ref="formRef" :rules="rules" :model="menuFormData" label-width="80px" label-position="right">
			<el-form-item label="菜单名称" prop="name">
				<el-input v-model="menuFormData.name" />
			</el-form-item>
			<el-form-item label="父级菜单" prop="parent">
				<el-input v-model="menuFormData.parent" />
			</el-form-item>
			<el-form-item label="图标" prop="icon">
				<IconSelector clearable v-model="menuFormData.icon" />
			</el-form-item>

			<el-row>
				<el-col :span="12">
					<el-form-item label="状态">
						<el-switch v-model="menuFormData.status" width="60" inline-prompt active-text="启用" inactive-text="禁用" />
					</el-form-item>
				</el-col>
				<el-col :span="12">
					<el-form-item v-if="menuFormData.status" label="侧边显示">
						<el-switch v-model="menuFormData.visible" width="60" inline-prompt active-text="显示" inactive-text="隐藏" />
					</el-form-item>
				</el-col>
			</el-row>

			<el-form-item label="菜单状态">
				<el-radio-group v-model="menuFormData.menu_status">
					<el-radio-button label="1">常规</el-radio-button>
					<el-radio-button label="2">目录</el-radio-button>
					<el-radio-button label="3">外链接</el-radio-button>
				</el-radio-group>
			</el-form-item>

			<el-form-item label="备注">
				<el-input v-model="menuFormData.description" maxlength="200" show-word-limit type="textarea" />
			</el-form-item>

			<el-divider></el-divider>

			<div style="min-height: 184px">
				<el-form-item v-if="menuFormData.menu_status === '3'" label="Url">
					<el-input v-model="menuFormData.web_path" />
				</el-form-item>

				<el-form-item v-if="menuFormData.menu_status === '1'" label="路由地址">
					<el-input v-model="menuFormData.web_path" />
				</el-form-item>

				<el-form-item v-if="menuFormData.menu_status === '1'" label="组件名称">
					<el-input v-model="menuFormData.component_name" />
				</el-form-item>

				<el-form-item v-if="menuFormData.menu_status === '1'" label="组件地址">
					<el-autocomplete
						class="w-full"
						v-model="menuFormData.component"
						:fetch-suggestions="querySearch"
						:trigger-on-focus="false"
						clearable
						:debounce="100"
						placeholder="输入组件地址"
					/>
				</el-form-item>

				<el-form-item v-if="menuFormData.menu_status === '1'" label="缓存">
					<el-switch v-model="menuFormData.cache" width="60" inline-prompt active-text="启用" inactive-text="禁用" />
				</el-form-item>
			</div>

			<el-divider></el-divider>
		</el-form>

		<div class="menu-form-btns">
			<el-button @click="handleSubmit" type="primary">保存</el-button>
			<el-button @click="handleCancel">取消</el-button>
		</div>
	</div>
</template>

<script lang="ts" setup>
import { ref, onMounted, reactive } from 'vue';
import { ElForm, FormRules } from 'element-plus';
import IconSelector from '/@/components/iconSelector/index.vue';
import { MenuFormDataType, MenuTreeItemType, ComponentFileItem } from '../../types';

interface IProps {
	initFormData: Partial<MenuTreeItemType> | null;
}

const validateWebPath = (rule: any, value: string, callback: Function) => {
	let pattern = /^\/.*?/;
	if (!pattern.test(value)) {
		callback(new Error('请输入正确的地址'));
	} else {
		callback();
	}
};

const props = withDefaults(defineProps<IProps>(), {
	initFormData: () => null,
});
const emit = defineEmits(['drawerClose']);

const formRef = ref<InstanceType<typeof ElForm>>();

const rules = reactive<FormRules>({
	web_path: [{ validator: validateWebPath, trigger: 'blur' }],
	name: [{ required: true, message: '菜单名称必填', trigger: 'blur' }],
	parent: [{ required: true, message: '父级菜单必选', trigger: ['blur', 'change'] }],
});

let menuFormData = reactive<MenuFormDataType>({
	parent: '',
	name: '',
	component: '',
	web_path: '',
	icon: '',
	cache: true,
	status: true,
	visible: true,
	menu_status: '1',
	component_name: '',
	description: '',
});

const setMenuFormData = () => {
	if (props.initFormData?.id) {
		menuFormData.id = props.initFormData?.id || '';
		menuFormData.name = props.initFormData?.name || '';
		menuFormData.parent = props.initFormData?.parent || '';
		menuFormData.component = props.initFormData?.component || '';
		menuFormData.web_path = props.initFormData?.web_path || '';
		menuFormData.icon = props.initFormData?.icon || '';
		menuFormData.status = props.initFormData?.status || true;
		menuFormData.visible = props.initFormData?.visible || true;
		menuFormData.cache = props.initFormData?.cache || true;
		menuFormData.component_name = props.initFormData?.component_name || '';
		menuFormData.description = props.initFormData?.description || '';
	}
};

const querySearch = (queryString: string, cb: any) => {
	const files: any = import.meta.glob('@views/**/*.vue');
	let fileLists: Array<any> = [];
	Object.keys(files).forEach((queryString: string) => {
		fileLists.push({
			label: queryString.replace(/(\.\/|\.vue)/g, ''),
			value: queryString.replace(/(\.\/|\.vue)/g, ''),
		});
	});
	const results = queryString ? fileLists.filter(createFilter(queryString)) : fileLists;
	// 统一去掉/src/views/前缀
	results.forEach((val) => {
		val.label = val.label.replace('/src/views/', '');
		val.value = val.value.replace('/src/views/', '');
	});
	cb(results);
};

const createFilter = (queryString: string) => {
	return (file: ComponentFileItem) => {
		return file.value.toLowerCase().indexOf(queryString.toLowerCase()) !== -1;
	};
};

const handleSubmit = () => {};

const handleCancel = (type: string = '') => {
	emit('drawerClose', type);
	formRef.value?.resetFields();
};

onMounted(async () => {
	setMenuFormData();
});
</script>

<style lang="scss" scoped>
.menu-form-com {
	border-radius: 8px;
	margin: 10px;
	overflow-y: auto;
	.menu-form-alert {
		color: #fff;
		line-height: 24px;
		padding: 8px 16px;
		margin-bottom: 20px;
		border-radius: 4px;
		background-color: var(--el-color-primary);
	}
	.menu-form-btns {
		padding-bottom: 10px;
		box-sizing: border-box;
	}
}
</style>
