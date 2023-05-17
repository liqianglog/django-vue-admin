<template>
    <fs-page>
        <splitpanes>
            <pane max-size="20" min-size="16">
                <el-card :body-style="{ height: '100%' }">
                    <p class="font-mono font-black text-center text-xl pb-5">
                        菜单列表
                        <el-tooltip effect="dark" :content="content" placement="right">
                            <el-icon>
                                <QuestionFilled/>
                            </el-icon>
                        </el-tooltip>
                    </p>
                    <el-input v-model="filterText" :placeholder="placeholder"/>
                    <el-tree ref="treeRef" class="font-mono font-bold leading-6 text-7xl" :data="data"
                             :props="treeProps"
                             :filter-node-method="filterNode" :load="loadNode" :allow-drag="allowDrag"
                             :allow-drop="allowDrop"
                             @node-drop="nodeDrop" lazy icon="ArrowRightBold" :indent="12" draggable
                             @node-click="handleNodeClick">
                        <template #default="{ node, data }">
							<span v-if="data.status" class="text-center font-black text-xl">
								<SvgIcon :name="node.data.icon"/>&nbsp;{{ node.label }}
							</span>
                            <span v-else class="text-center font-black text-xl text-red-700">
								<SvgIcon :name="node.data.icon"/>&nbsp;{{ node.label }}
							</span>
                        </template>
                    </el-tree>
                </el-card>
            </pane>
            <pane min-size="30">
                <el-card :body-style="{ height: '100%' }">
                    <el-form ref="formRef" :rules="rules" :model="form" label-width="80px"
                             label-position="right">
                        <el-alert :title="content" type="success" effect="dark" :closable="false" center/>
                        <el-divider>
                            <strong>菜单配置</strong>
                        </el-divider>
                        <el-form-item label="菜单ID" prop="id">
                            <el-input v-model="form.id" disabled/>
                        </el-form-item>
                        <el-form-item label="父级ID" prop="parent">
                            <el-input v-model="form.parent"/>
                        </el-form-item>
                        <el-form-item required label="菜单名称" prop="name">
                            <el-input v-model="form.name"/>
                        </el-form-item>
                        <el-form-item label="组件地址" prop="component">
                            <el-autocomplete class="w-full" v-model="form.component"
                                             :fetch-suggestions="querySearch" :trigger-on-focus="false"
                                             clearable
                                             debounce="100"
                                             placeholder="输入组件地址"/>
                        </el-form-item>
                        <el-form-item required label="Url" prop="web_path">
                            <el-input v-model="form.web_path"/>
                        </el-form-item>
                        <el-form-item label="排序" prop="sort">
                            <el-input-number v-model="form.sort" controls-position="right"/>
                        </el-form-item>
                        <el-form-item label="状态">
                            <el-radio-group v-model="form.status">
                                <el-radio :label="true">启用</el-radio>
                                <el-radio :label="false">禁用</el-radio>
                            </el-radio-group>
                        </el-form-item>
                        <el-form-item label="侧边可见">
                            <el-radio-group v-model="form.visible">
                                <el-radio :label="true">启用</el-radio>
                                <el-radio :label="false">禁用</el-radio>
                            </el-radio-group>
                        </el-form-item>
                        <el-form-item label="缓存">
                            <el-radio-group v-model="form.cache">
                                <el-radio :label="true">启用</el-radio>
                                <el-radio :label="false">禁用</el-radio>
                            </el-radio-group>
                        </el-form-item>
                        <el-form-item label="图标" prop="icon">
                            <IconSelector clearable v-model="form.icon"/>
                        </el-form-item>
                    </el-form>
                    <el-divider></el-divider>
                    <div>
                        <el-button @click="saveMenu()" type="primary" round>保存</el-button>
                        <el-button @click="newMenu()" type="success" round :disabled="!form.id">新建</el-button>
                        <el-button @click="addChildMenu()" type="warning" round :disabled="!form.id">添加子级
                        </el-button>
                        <!--            <el-button @click="addSameLevelMenu()" type="warning" round>添加同级</el-button>-->
                        <el-button @click="deleteMenu()" type="danger" round :disabled="!form.id">删除菜单
                        </el-button>
                    </div>
                </el-card>
            </pane>
            <pane min-size="30">
                <el-card :body-style="{ height: '100%' }">
                    <menuButton :select-menu="form"/>
                </el-card>
            </pane>
        </splitpanes>
    </fs-page>
</template>

<script lang="ts" setup name="menu">
import {Splitpanes, Pane} from 'splitpanes';
import 'splitpanes/dist/splitpanes.css';
import * as api from './api';
import * as menuButoonApi from './components/menuButton/api';
import {ElForm, ElTree, FormRules, ElMessageBox} from 'element-plus';
import {ref, onMounted, watch, reactive, toRaw, defineAsyncComponent, nextTick, shallowRef, onActivated} from 'vue';
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

interface ComponentFileItem {
    value: string;
    label: string;
}

// 引入组件
const menuButton = defineAsyncComponent(() => import('./components/menuButton/index.vue'));
const IconSelector = defineAsyncComponent(() => import('/@/components/iconSelector/index.vue'));
const SvgIcon = defineAsyncComponent(() => import('/@/components/svgIcon/index.vue'));
const placeholder = ref('请输入菜单名称');
const filterText = ref('');
const treeRef = ref<InstanceType<typeof ElTree>>();

const treeProps = {
    children: 'children',
    label: 'name',
    icon: 'icon',
    isLeaf: (data: Tree[], node: Node) => {
        // @ts-ignore
        if (node.data.is_catalog) {
            return false;
        } else {
            return true;
        }
    },
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
        api.lazyLoadMenu({parent: node.data.id}).then((res: APIResponseData) => {
            resolve(res.data);
        });
    }
};

// 判断是否可以拖动
const allowDrag = (node: Node) => {
    // @ts-ignore
    if (node.data.is_catalog) {
        return false;
    } else {
        return true;
    }
};

// 判断是否可以被放置
const allowDrop = (draggingNode: Node, dropNode: Node, type: string) => {
    // @ts-ignore
    if (!dropNode.isLeaf) {
        return true;
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

let isAddNewMenu = ref(false); // 判断当前是新增菜单，还是更新保存当前菜单

const permissionDrawerVisible = ref(false);

const content = `
1.红色菜单代表状态禁用;
2.添加菜单，如果是目录，组件地址为空即可;
3.添加根节点菜单，父级ID为空即可;
4.支持拖拽菜单;
`;

let form: Form<any> = reactive({
    id: '',
    parent: '',
    name: '',
    component: '',
    web_path: '',
    sort: '',
    status: true,
    is_catalog: false,
    permission: '',
    icon: '',
    visible: true,
    cache: true,
});

let menuPermissonList = ref([]);

const formRef = ref<InstanceType<typeof ElForm>>();

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

const rules = reactive<FormRules>({
    // @ts-ignore
    web_path: [{validator: validateWebPath, trigger: 'blur'}],
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

const getPermissions = (menu: object) => {
    menuButoonApi.GetList(menu).then((res: APIResponseData) => {
        menuPermissonList.value = res.data;
    });
};

const saveMenu = () => {
    formRef.value?.validate((valid, fields) => {
        if (valid) {
            if (!isAddNewMenu.value) {
                // 保存菜单

                form.component == '' ? (form.is_catalog = true) : (form.is_catalog = false);
                api.UpdateObj(form).then((res: APIResponseData) => {
                    successMessage(res.msg as string);
                    getData();
                });
            } else {
                // 新增菜单
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

    // 点击tree node时，加载对应的权限菜单
    // getPermissions({ menu: form.id });
};

const addPermission = () => {
    !form.is_catalog ? (permissionDrawerVisible.value = true) : errorMessage('目录没有菜单权限');
};
const drawerClose = () => {
    permissionDrawerVisible.value = false;
};

// 页面打开后获取列表数据
onMounted(() => {
    getData();
});
onActivated(() => {
    console.log('keep-alive成功')
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
