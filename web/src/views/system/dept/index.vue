<template>
    <fs-page>
        <splitpanes>
            <pane max-size="20">
                <el-card :body-style="{ height: '100%' }">
                    <p class="font-mono font-black text-center text-xl pb-5">部门列表</p>
                    <el-input v-model="filterText" :placeholder="placeholder"/>
                    <el-tree
                        ref="treeRef"
                        class="font-mono font-bold leading-6 text-7xl"
                        :data="data"
                        :props="treeProps"
                        :filter-node-method="filterNode"
                        :load="loadNode"
                        @node-drop="nodeDrop"
                        lazy
                        icon="ArrowRightBold"
                        :indent="12"
                        draggable
                        @node-click="handleNodeClick"
                    >
                        <template #default="{ node, data }">
                            <span v-if="data.status" class="text-center font-black text-xl"><SvgIcon
                                :name="node.data.icon"/>&nbsp;{{ node.label }}</span>
                            <span v-else class="text-center font-black text-xl text-red-700"><SvgIcon
                                :name="node.data.icon"/>&nbsp;{{ node.label }}</span>
                        </template>
                    </el-tree>
                </el-card>
            </pane>
            <pane>
                <el-card :body-style="{ height: '100%' }">
                    <el-form ref="formRef" :rules="rules" :model="form" label-width="120px" label-position="right">
                        <el-divider>
                            <strong>部门配置</strong>
                        </el-divider>
                        <el-row>
                            <el-col :span="10">
                                <el-form-item label="部门ID" prop="id">
                                    <el-input v-model="form.id" disabled/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="10">
                                <el-form-item label="父级部门ID" prop="parent">
                                    <el-input v-model="form.parent"/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="10">
                                <el-form-item required label="部门名称" prop="name">
                                    <el-input v-model="form.name"/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="10">
                                <el-form-item required label="部门标识" prop="key">
                                    <el-input v-model="form.key"/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="10">
                                <el-form-item label="负责人" prop="owner">
                                    <el-input v-model="form.owner"/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="10">
                                <el-form-item label="联系电话" prop="phone">
                                    <el-input v-model="form.phone"/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="10">
                                <el-form-item label="邮箱" prop="email">
                                    <el-input v-model="form.email"/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="10">
                                <el-form-item label="排序" prop="sort">
                                    <el-input-number v-model="form.sort" controls-position="right"/>
                                </el-form-item>
                            </el-col>

                            <el-col class="center">
                                <el-divider>
                                    <el-button @click="saveMenu()" type="primary" round>保存</el-button>
                                    <el-button @click="newMenu()" type="success" round :disabled="!form.id">新建
                                    </el-button>
                                    <el-button @click="addChildMenu()" type="info" round :disabled="!form.id">添加子级
                                    </el-button>
                                    <el-button @click="addSameLevelMenu()" type="warning" round :disabled="!form.id">
                                        添加同级
                                    </el-button>
                                    <el-button @click="deleteMenu()" type="danger" round :disabled="!form.id">删除部门
                                    </el-button>
                                </el-divider>
                            </el-col>
                        </el-row>
                    </el-form>
                </el-card>
            </pane>
        </splitpanes>
    </fs-page>
</template>

<script lang="ts" setup>
import {Splitpanes, Pane} from 'splitpanes';
import 'splitpanes/dist/splitpanes.css';
import * as api from './api';
import {ElForm, ElMessageBox, ElTree, FormRules} from 'element-plus';
import {ref, onMounted, reactive, toRaw, watch} from 'vue';
import XEUtils from 'xe-utils';
import {errorMessage, successMessage} from '../../../utils/message';

interface Tree {
    id: number;
    name: string;
    status: boolean;
    children?: Tree[];
}

interface APIResponseData {
    code?: number;
    data: [];
    msg?: string;
}

interface Form<T> {
    [key: string]: T;
}

const placeholder = ref('请输入部门名称');
const filterText = ref('');
const treeRef = ref<InstanceType<typeof ElTree>>();

const treeProps = {
    children: 'children',
    label: 'name',
    // isLeaf: (data: Tree[], node: Node) => {
    // 	// @ts-ignore
    // 	if (node.data.is_catalog) {
    // 		return false;
    // 	} else {
    // 		return true;
    // 	}
    // },
};

const validateWebPath = (rule: string, value: string, callback: Function) => {
    let pattern = /^\/.*?/;
    if (!pattern.test(value)) {
        callback(new Error('请输入正确的地址'));
    } else {
        callback();
    }
};

watch(filterText, (val) => {
    treeRef.value!.filter(val);
});

const filterNode = (value: string, data: Tree) => {
    if (!value) return true;
    return toRaw(data).name.indexOf(value) !== -1;
};

// 懒加载
const loadNode = (node: Node, resolve: (data: Tree[]) => void) => {
    // @ts-ignore
    if (node.level !== 0) {
        // @ts-ignore
        api.lazyLoadDept({parent: node.data.id}).then((res: APIResponseData) => {
            resolve(res.data);
        });
    }
};

const nodeDrop = (draggingNode: Node, dropNode: Node, dropType: string, event: any) => {
    // @ts-ignore
    if (!dropNode.isLeaf) {
        // @ts-ignore
        api.dragMenu({menu_id: draggingNode.data.id, parent_id: dropNode.data.id}).then((res: APIResponseData) => {
            successMessage(res.msg as string);
        });
    }
};

let data = ref([]);

let isAddNewMenu = ref(false); // 判断当前是新增部门，还是更新保存当前部门

let form: Form<any> = reactive({
    id: '',
    parent: '',
    name: '',
    owner: '',
    phone: '',
    email: '',
    sort: '',
});

const formRef = ref<InstanceType<typeof ElForm>>();

const rules = reactive<FormRules>({
    // @ts-ignore
    name: [{required: true, message: '部门名称必填', trigger: 'blur'}],
    key: [{required: true, message: '部门标识必填', trigger: 'blur'}],
});

const getData = () => {
    api.GetList({}).then((ret: APIResponseData) => {
        const responseData = ret.data;
        const result = XEUtils.toArrayTree(responseData, {
            parentKey: 'parent',
            children: 'children',
            strict: true,
        });
        data.value = result;
    });
};

const saveMenu = () => {
    formRef.value?.validate((valid, fields) => {
        if (valid) {
            if (!isAddNewMenu.value) {
                // 保存部门
                form.component == '' ? (form.is_catalog = true) : (form.is_catalog = false);
                api.UpdateObj(form).then((res: APIResponseData) => {
                    successMessage(res.msg as string);
                    getData();
                });
            } else {
                // 新增部门
                form.component == '' ? (form.is_catalog = true) : (form.is_catalog = false);
                api.AddObj(form).then((res: APIResponseData) => {
                    successMessage(res.msg as string);
                    getData();
                });
            }
        } else {
            errorMessage('请填写检查表单');
        }
    });
};

const newMenu = () => {
    formRef.value?.resetFields();
    isAddNewMenu.value = true;
};

const addChildMenu = () => {
    let parentId = form.id;
    formRef.value?.resetFields();
    form.parent = parentId;
    isAddNewMenu.value = true;
};

const addSameLevelMenu = () => {
    let parentId = form.parent;
    formRef.value?.resetFields();
    form.parent = parentId;
    isAddNewMenu.value = true;
};

const deleteMenu = () => {
    ElMessageBox.confirm(
        '您确认删除该菜单项吗?',
        '温馨提示',
        {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'warning',
        }
    ).then(() => {
        api.DelObj(form).then((res: APIResponseData) => {
            successMessage(res.msg as string);
            getData();
        });
    })

};

const handleNodeClick = (data: any, node: any, prop: any) => {
    Object.keys(toRaw(data)).forEach((key: string) => {
        form[key] = data[key];
    });
    delete form.component_name;
    form.id = data.id;
    isAddNewMenu.value = false;
};

// 页面打开后获取列表数据
onMounted(() => {
    getData();
});
</script>

<style lang="scss" scoped>
.el-row {
    height: 100%;

    .el-col {
        height: 100%;
    }
}

.el-card {
    height: 100%;
}
</style>
