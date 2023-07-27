<template>
  <el-form ref="formRef" :rules="rules" :model="deptFormData" label-width="100px" label-position="right"
    class="dept-form-com">
    <el-form-item label="部门ID" prop="id">
      <el-input v-model="deptFormData.id" disabled />
    </el-form-item>
    <el-form-item label="父级部门ID" prop="parent">
      <el-input v-model="deptFormData.parent" />
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
    <el-form-item label="联系电话" prop="phone">
      <el-input v-model="deptFormData.phone" />
    </el-form-item>
    <el-form-item label="邮箱" prop="email">
      <el-input v-model="deptFormData.email" />
    </el-form-item>
    <el-form-item label="排序" prop="sort">
      <el-input-number v-model="deptFormData.sort" controls-position="right" />
    </el-form-item>
    <el-form-item>
      <el-button @click="handleUpdateMenu('update')" type="primary" :disabled="deptBtnLoading">保存</el-button>
      <el-button @click="handleClose">取消
      </el-button>
    </el-form-item>

  </el-form>
</template>

<script lang="ts" setup>
import { reactive, ref, onMounted } from 'vue';
import { ElForm, FormRules } from 'element-plus';
import { DeptFormDataType, TreeItemType } from '../types';

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
})
const emit = defineEmits(['drawerClose'])

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

const handleUpdateMenu = (type: string) => { };

const handleClose = () => {
  emit('drawerClose')
  formRef.value?.resetFields();
};

onMounted(() => {
  console.log(props.initFormData?.id, '----');
})
</script>

<style lang="scss" scoped>
.dept-form-com {
  height: 100%;
  padding: 20px;
  box-sizing: border-box;
}
</style>