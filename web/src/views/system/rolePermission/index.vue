<template>
    <el-drawer
        size="70%"
        v-model="drawer"
        direction="rtl"
        destroy-on-close
        :before-close="handleClose"
    >
        <template #header>
            <div>
                <el-tag size="large" type="primary">当前角色:{{ editedRoleInfo.name }}</el-tag>
            </div>
        </template>
        <div style="padding: 1em">
            <el-row :gutter="10">
                <el-col :xs="24" :sm="24" :md="8" :lg="6" :xl="6">
                    <el-card header="菜单页面授权">
                        <template #header>
                            <div class="card-header">
                                <el-tooltip effect="dark" content="点击菜单项,可对菜单下的按钮/接口授权"
                                            placement="right">
                                    <div>
                                        <span>菜单页面</span>
                                        <el-icon>
                                            <QuestionFilled/>
                                        </el-icon>
                                    </div>
                                </el-tooltip>
                                <el-button size="mini" type="primary" @click="onSaveAuth">保存菜单授权</el-button>
                            </div>
                        </template>
                        <el-tree :data="menuData"
                                 ref="menuTree"
                                 show-checkbox
                                 node-key="id"
                                 highlight-current
                                 :expand-on-click-node="false"
                                 :check-on-click-node="true"
                                 :props="defaultProps"
                                 @node-click="menuNodeClick"
                        />
                    </el-card>
                </el-col>
                <el-col :xs="24" :sm="24" :md="16" :lg="18" :xl="18">
                    <!--          <el-alert title="对页面菜单下按钮授权"  description="新增或删除对菜单下的按钮/接口授权" type="warning" />-->
                    <el-card v-if="isBtnPermissionShow">
                        <template #header>
                            <div class="card-header">
                                <el-tooltip effect="dark" content="新增或删除对菜单下的按钮/接口授权" placement="right">
                                    <div>
                                        <span>按钮/接口授权</span>
                                        <el-icon>
                                            <QuestionFilled/>
                                        </el-icon>
                                    </div>
                                </el-tooltip>
                            </div>
                        </template>
                        <div>
                            <el-divider content-position="left">{{ editedMenuInfo.name }}</el-divider>
                            <el-button type="primary" size="small" style="margin-bottom: 0.5em"
                                       @click="createBtnPermission">新增
                            </el-button>
                            <el-table size="small" :data="buttonPermissionData" border style="width: 100%">
                                <el-table-column prop="menu_button" label="权限名称" width="100">
                                    <template #default="scope">
                                        <div>{{ formatMenuBtn(scope.row.menu_button) }}</div>
                                    </template>
                                </el-table-column>
                                <el-table-column prop="data_range" label="权限范围" width="140">
                                    <template #default="scope">
                                        <div>{{ formatDataRange(scope.row.data_range) }}</div>
                                    </template>
                                </el-table-column>
                                <el-table-column prop="dept" label="权限涉及部门"/>
                                <el-table-column fixed="right" label="操作" width="120">
                                    <template #default="scope">
                                        <el-button type="danger" size="small" @click="onDeleteBtn(scope)">删除
                                        </el-button>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </div>


                        <!--          <el-divider content-position="left">字段授权</el-divider>-->
                        <!--          <el-table size="small" :data="crudPermissionData" border style="width: 100%">-->
                        <!--            <el-table-column prop="field" label="字段"></el-table-column>-->
                        <!--            <el-table-column prop="table" label="列表显示">-->
                        <!--              <template #default="scope">-->
                        <!--                <div>-->
                        <!--                  <el-switch size="mini" v-model="scope.row.table"/>-->
                        <!--                </div>-->
                        <!--              </template>-->
                        <!--            </el-table-column>-->
                        <!--            <el-table-column prop="view" label="表单查看">-->
                        <!--              <template #default="scope">-->
                        <!--                <div>-->
                        <!--                  <el-switch size="mini" v-model="scope.row.view"/>-->
                        <!--                </div>-->
                        <!--              </template>-->
                        <!--            </el-table-column>-->
                        <!--            <el-table-column prop="edit" label="表单编辑">-->
                        <!--              <template #default="scope">-->
                        <!--                <div>-->
                        <!--                  <el-switch size="mini" v-model="scope.row.edit"/>-->
                        <!--                </div>-->
                        <!--              </template>-->
                        <!--            </el-table-column>-->
                        <!--          </el-table>-->
                    </el-card>
                </el-col>
            </el-row>
            <el-dialog v-model="dialogFormVisible" width="400px" title="配置按钮权限">
                <el-form ref="buttonFormRef" :model="buttonForm" :rules="buttonRules" label-width="120px">
                    <el-form-item label="按钮" prop="menu_button">
                        <el-select v-model="buttonForm.menu_button" placeholder="请选择按钮" @change="onChangeButton">
                            <el-option v-for="(item,index) in buttonOptions" :key="index" :label="item.name"
                                       :value="item.id"/>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="权限范围" prop="data_range">
                        <el-select v-model="buttonForm.data_range" placeholder="请选择按钮">
                            <el-option v-for="(item,index) in dataScopeOptions" :key="index" :label="item.label"
                                       :value="item.value"/>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="数据部门" prop="dept" v-show="buttonForm.data_range === 4">
                        <div class="dept-tree">
                            <el-tree
                                :data="deptOptions"
                                show-checkbox
                                default-expand-all
                                :default-checked-keys="deptCheckedKeys"
                                ref="deptTree"
                                node-key="id"
                                :check-strictly="true"
                                :props="{ label: 'name' }"
                            ></el-tree>
                        </div>
                    </el-form-item>
                </el-form>
                <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="onSaveButtonForm">
          确定
        </el-button>
      </span>
                </template>
            </el-dialog>
        </div>
    </el-drawer>
</template>

<script lang="ts" setup name="rolePermission">
import {ref, defineExpose, reactive, toRefs} from 'vue'
import {ElMessageBox} from 'element-plus'
import * as api from './api'
import type {FormRules, FormInstance} from 'element-plus'
import {ElMessage} from 'element-plus'
import XEUtils from 'xe-utils'
//抽屉是否显示
const drawer = ref(false)
//当前编辑的角色信息
const editedRoleInfo = ref({})

//抽屉关闭确认
const handleClose = (done: () => void) => {
    ElMessageBox.confirm('您确定要关闭?', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
    })
        .then(() => {
            done()
        })
        .catch(() => {
            // catch error
        })
}

/*****菜单的配置项***/
const defaultProps = {
    children: 'children',
    label: 'name',
    isLeaf: 'hasChild'
}

interface Tree {
    name: string
    children?: Tree[],
    id: number
}

let menuData = ref<Tree>()
//获取菜单
const getMenuData = () => {
    api.GetMenu({}).then((res: any) => {
        const {data} = res
        const list = XEUtils.toArrayTree(data, {parentKey: "parent", key:'menu_id',strict: true})
        menuData.value = list
    })
}

let isBtnPermissionShow = ref(false)
let buttonOptions = ref<[]>()
let editedMenuInfo = ref()
//菜单节点点击事件
const menuNodeClick = (node: any, obj: any) => {
    isBtnPermissionShow.value = !node.is_catalog
    if (!node.is_catalog) {
        buttonOptions.value = []
        editedMenuInfo.value = node
        api.GetMenuButton({menu: node.menu_id}).then((res: any) => {
            const {data} = res
            buttonOptions.value = data
        })
        api.getObj({menu: node.menu_id, role: editedRoleInfo.value.id}).then((res: any) => {
            const {data} = res
            buttonPermissionData.value = data
        })
    }

}
const menuTree = ref()
/*****菜单的配置项***/
/***按钮授权的弹窗****/
//是否显示新增表单
const dialogFormVisible = ref(false)
//部门树
const deptTree = ref()
//自定义部门数据
const deptOptions = ref()
//选中的部门数据
const deptCheckedKeys = []
//按钮表单
const buttonForm = reactive({
    menu_button: null,
    role: null,
    menu: null,
    data_range: null,
    dept: []
})
//按钮表格数据
let buttonPermissionData = ref([])
//按钮表单验证
const buttonRules = reactive<FormRules>({
    menu_button: [
        {required: true, message: '必填项'}
    ],
    data_range: [
        {required: true, message: '必填项'}
    ]
})
//新增按钮
const buttonFormRef = ref<FormInstance>()
const createBtnPermission = () => {
    dialogFormVisible.value = true
    buttonForm.menu_button = null
    buttonForm.menu = null
    buttonForm.role = null
    buttonForm.data_range = null
    buttonForm.dept = []
}
//权限范围数据
const dataScopeOptions = ref<[]>()
//按钮值变化事件
const onChangeButton = (val: any) => {
    dataScopeOptions.value = []
    //获取权限值范围
    api.GetDataScope({menu_button: val}).then((res: any) => {
        dataScopeOptions.value = res.data
    })
    //获取权限部门值
    api.GetDataScopeDept({menu_button: val}).then((res: any) => {
        deptOptions.value = XEUtils.toArrayTree(res.data, {parentKey: 'parent', strict: false})
    })

}
//过滤按钮名称
const formatMenuBtn = (val: any) => {
    let obj: any = buttonOptions.value?.find((item: any) => {
        return item.id === val
    })
    return obj ? obj.name : null
}
//过滤权限范围
const formatDataRange = (val: any) => {
    let obj: any = [
        {
            "value": 0,
            "label": '仅本人数据权限'
        },
        {
            "value": 1,
            "label": '本部门及以下数据权限'
        },
        {
            "value": 2,
            "label": '本部门数据权限'
        },
        {
            "value": 3,
            "label": '全部数据权限'
        },
        {
            "value": 4,
            "label": '自定义数据权限'
        }
    ].find((item: any) => {
        return item.value === val
    })
    return obj ? obj.label : null
}
//保存按钮表单

const onSaveButtonForm = async () => {
    const {id: roleId} = editedRoleInfo.value
    const {id: menuId} = editedMenuInfo.value
    const form: any = Object.assign({}, buttonForm)
    form.role = roleId
    form.menu = menuId
    //选中的部门
    const checkedList = deptTree.value.getCheckedKeys()
    form.dept = checkedList
    if (!buttonFormRef.value) return
    await buttonFormRef.value.validate((valid, fields) => {
        if (valid) {
            api.CreatePermission(form).then((res: any) => {
                const {data} = res
                buttonPermissionData.value.push(data)
                dialogFormVisible.value = false
                ElMessage({
                    type: 'success',
                    message: res.msg,
                })
            })
        } else {
            ElMessage({
                type: 'error',
                title: '提交错误',
                message: 'F12控制台看详情',
            })
            console.log('提交错误', fields)
        }
    })

}
//删除按钮权限
const onDeleteBtn = (scope: any) => {
    const {row, $index} = scope
    ElMessageBox.confirm(
        '您是否要删除数据?',
        '温馨提示',
        {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
        }
    ).then(() => {
        api.DeletePermission({id: row.id}).then((res: any) => {
            buttonPermissionData.value.splice($index, 1)
            ElMessage({
                type: 'success',
                message: res.msg,
            })
        })
    })
        .catch(() => {
            ElMessage({
                type: 'info',
                message: '取消删除',
            })
        })

}
/***按钮授权的弹窗****/
//初始化数据
const initGet = () => {
    getMenuData()
}

/**
 * 保存授权
 */
const onSaveAuth = () => {
    //选中的菜单
    const checkedList = menuTree.value.getCheckedKeys()
    //半选中的菜单
    const halfCheckedList = menuTree.value.getHalfCheckedKeys()
    //合并的菜单数据
    const menuIdList = [...checkedList, ...halfCheckedList]
    // console.log(menuIdList)
    const {id: roleId} = editedRoleInfo.value
    const data = {
        role: roleId,
        menu: menuIdList
    }
    api.SaveMenuPermission(data).then((res: any) => {
        ElMessage({
            message: res.msg,
            type: 'success',
        })
    })
}


defineExpose({drawer, editedRoleInfo, initGet})
</script>

<style scoped>
.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.dept-tree::-webkit-scrollbar {
    display: none; /* Chrome Safari */
}

.dept-tree {
    height: 160px;
    overflow-y: scroll;
    scrollbar-width: none; /* firefox */
    -ms-overflow-style: none; /* IE 10+ */
    border: 1px solid #e1e1e1;
    width: 16em;
    border-radius: 2px;
}
</style>
