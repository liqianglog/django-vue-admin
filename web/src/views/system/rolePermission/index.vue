<template>
  <el-drawer
      size="70%"
      v-model="drawer"
      direction="rtl"
      destroy-on-close
      :before-close="handleClose"
  >
    <template #header>
      <el-button-group>
        <el-button size="mini" plain type="primary">当前角色:{{editedRoleInfo.name}}</el-button>
        <el-button size="mini" type="primary" @click="onSaveAuth">保存授权</el-button>
      </el-button-group>
    </template>
    <div style="padding: 1em">
    <el-row :gutter="10">
      <el-col :xs="24" :sm="24" :md="8" :lg="6" :xl="6">
        <el-card header="页面菜单">
          <el-tree :data="menuData"
                   ref="menuTree"
                   show-checkbox
                   node-key="id"
                   highlight-current
                   :expand-on-click-node="false"
                   :check-on-click-node="true"
                   :props="defaultProps"
                   @current-change="menuNodeClick"
          />
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="24" :md="16" :lg="18" :xl="18">
        <el-card v-if="!isCatalog">
          <template #header>
            <div class="card-header">
              <span>页面授权</span>
            </div>
          </template>
          <div>
            <el-divider content-position="left">按钮授权</el-divider>
            <el-button type="primary" size="small" style="margin-bottom: 0.5em" @click="createBtnPermission">新增</el-button>
            <el-table size="small" :data="buttonPermissionData" border style="width: 100%">
              <el-table-column prop="name" label="权限名称" width="100"/>
              <el-table-column prop="datarange" label="权限范围" width="100"/>
              <el-table-column prop="dept" label="权限涉及部门"/>
              <el-table-column fixed="right" label="操作" width="120">
                <template #default>
                  <el-button type="danger" size="small">删除</el-button>
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
      <el-dialog v-model="dialogFormVisible" title="配置按钮权限">
        <el-form :model="buttonForm" :rules="buttonRules" label-width="120px">
          <el-form-item label="按钮">
            <el-select v-model="buttonForm.name" placeholder="请选择按钮" @change="onChangeButton">
              <el-option v-for="(item,index) in buttonOptions" :key="index" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="权限范围">
            <el-select v-model="buttonForm.data_range" placeholder="请选择按钮">
              <el-option v-for="(item,index) in dataScopeOptions" :key="index" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="数据部门"  v-show="buttonForm.data_range === 4">
            <div class="dept-tree">
              <el-tree
                  :data="deptOptions"
                  show-checkbox
                  default-expand-all
                  :default-checked-keys="deptCheckedKeys"
                  ref="dept"
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

<script lang="ts" setup>
import {ref, defineExpose,reactive,toRefs} from 'vue'
import {ElMessageBox} from 'element-plus'
import * as api from './api'
import type {  FormRules } from 'element-plus'
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
  isLeaf:'hasChild'
}

interface Tree {
  name: string
  children?: Tree[],
  id:number
}
let menuData= ref<Tree>()
//获取菜单
const getMenuData = () => {
  api.GetMenu({}).then((res:any)=>{
    const {data} = res
    const list = XEUtils.toArrayTree(data,{parentKey:"parent",strict:true})
    menuData.value = list
  })
}

let isCatalog = ref(true)
let buttonOptions = ref<[]>()
let checkedMenuId = ref()
//菜单节点点击事件
const menuNodeClick=(node:any)=>{
  isCatalog.value = node.is_catalog
  if(!node.is_catalog){
    buttonOptions.value = []
    checkedMenuId.value = node.id
    api.GetMenuButton({menu:node.id}).then((res:any)=>{
      const {data} = res
      buttonOptions.value = data
    })
  }

}
const menuTree = ref()
/*****菜单的配置项***/
/***按钮授权的弹窗****/
//是否显示新增表单
const dialogFormVisible = ref(false)
//自定义部门数据
const deptOptions = ref()
//选中的部门数据
const deptCheckedKeys=[]


//按钮表单
const buttonForm = reactive({
  menu_button:'',
  role:'',
  data_range:'',
  dept:[]
})
//按钮表单验证
const buttonRules = reactive<FormRules>({
  name:[
    { required: true, message: '必填项' }
  ],
  data_range:[
    { required: true, message: '必填项' }
  ]
})
//新增按钮
const createBtnPermission = ()=>{
  dialogFormVisible.value = true
}
//权限范围数据
const dataScopeOptions=ref<[]>()
//按钮值变化事件
const onChangeButton = (val:any)=>{
  dataScopeOptions.value = []
  //获取权限值范围
  api.GetDataScope({menu_button:val}).then((res:any)=>{
    dataScopeOptions.value = res.data
  })
}
//保存按钮表单
const onSaveButtonForm = ()=>{
  console.log(editedRoleInfo)
}
//按钮表格数据
const buttonPermissionData: any[] = [
  {
    name: "查询",
    datarange: 1,
    dept: ""
  }
]
/***按钮授权的弹窗****/
//初始化数据
const initGet = ()=>{
  getMenuData()
}


//字段权限
const crudPermissionData: any[] = [
  {
    field: "name",
    table: true,
    view: true,
    edit: true
  }
]

/**
 * 保存授权
 */
const onSaveAuth = ()=>{
  //选中的菜单
  const checkedList = menuTree.value.getCheckedKeys()
  //半选中的菜单
  const halfCheckedList = menuTree.value.getHalfCheckedKeys()
  //合并的菜单数据
  const menuIdList = [...checkedList,...halfCheckedList]
  console.log(menuIdList)
}


defineExpose({drawer,editedRoleInfo,initGet})
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
