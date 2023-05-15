<template>
  <fs-page style="padding: 10px">
    <el-card :body-style="{height:'100%'}">
      <el-tabs tab-position="left" class="demo-tabs" style="height: 70vh">
        <el-tab-pane label="全部">
          <div>
            <el-row>
              <el-col :soan="6" :offset="18">
                这里放搜索框
              </el-col>
            </el-row>
          </div>
          <div>
            <el-row :gutter="10">
              <el-col :span="3" v-for="(item,index) in fileList" :key="index">
                <el-image
                    style="width: 150px; height: 150px"
                    :src="formatImgUrl(item.url)"
                    :zoom-rate="1.2"
                    :preview-src-list="[item.url]"
                    :initial-index="4"
                    fit="fill"
                />
                <div>
                 <div> <el-text>{{item.name}}</el-text></div>
                  <div>
                    <el-popover
                        placement="bottom"
                        :width="500"
                        trigger="click"
                    >
                      <template #reference>
                        <el-button type="text">详细</el-button>
                      </template>
                      <div>
                        <el-descriptions
                        :column="2"
                        border
                        >
                          <el-descriptions-item label="文件名称">{{item.name}}</el-descriptions-item>
                          <el-descriptions-item label="创建人">{{item.creator_name}}</el-descriptions-item>
                          <el-descriptions-item label="创建时间">{{item.create_datetime}}</el-descriptions-item>
                        </el-descriptions>
                      </div>
                    </el-popover>
                    <el-popconfirm title="您确定要删除?" @confirm="onDel(item)">
                      <template #reference>
                        <el-button type="text">删除</el-button>
                      </template>
                    </el-popconfirm>

                  </div>
                </div>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>
        <el-tab-pane label="Config">Config</el-tab-pane>
        <el-tab-pane label="Role">Role</el-tab-pane>
        <el-tab-pane label="Task">Task</el-tab-pane>
      </el-tabs>
    <el-divider></el-divider>
    <el-row>
      <el-col :span="12" :offset="12">
        这里放分页
      </el-col>
    </el-row>
    </el-card>

  </fs-page>
</template>

<script lang="ts" setup>
import {DelObj, GetList} from "./api";
import {ref,onMounted} from "vue";
import {getBaseURL} from "/@/utils/baseUrl";
import {ElMessage} from "element-plus";
const fileList = ref([])
const getData = function (){
  GetList({}).then((res:any)=>{
    const {data} = res
    fileList.value = data
  })
}

const onDel = function (item:any) {
  DelObj(item.id).then((res:any)=>{
    ElMessage.success("删除成功！");
    getData()
  })
}
const formatImgUrl = function (src:string) {
  return getBaseURL()+src
}


onMounted(()=>{
  getData()
})
</script>
<style scoped>
.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}

.el-tabs--right .el-tabs__content,
.el-tabs--left .el-tabs__content {
  height: 100%;
}
.el-tabs__nav-scroll{
  border-right: 1px solid #efefef;
}
</style>
