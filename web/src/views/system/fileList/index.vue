<template>
  <fs-page>
      <el-row style="margin: 10px">
        <el-col :span="6" :offset="18">
          <el-input
              class="w-60"
              placeholder="请输入名称"
              v-model="fileParams.name"
              @keyup.enter="getData"
              clearable
              @blur="getData"
          >
            <template #append>
              <el-button :icon="Search" @click="getData">
              </el-button>
            </template>
          </el-input>
        </el-col>
      </el-row>
    <el-row :gutter="10" style="height: 65vh;margin: 10px">
      <el-col :span="3" v-for="(item,index) in fileList" :key="index">
        <el-card>
          <el-image
              style="width: 150px; height: 150px"
              :src="formatImgUrl(item.url)"
              :zoom-rate="1.2"
              :preview-src-list="[formatImgUrl(item.url)]"
              :initial-index="4"
              fit="fill"
          />
          <div>
            <el-text>{{ item.name }}</el-text>
          </div>
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
                  <el-descriptions-item label="文件名称">{{ item.name }}</el-descriptions-item>
                  <el-descriptions-item label="创建人">{{ item.creator_name }}</el-descriptions-item>
                  <el-descriptions-item label="存储引擎">{{ item.engine }}</el-descriptions-item>
                  <el-descriptions-item label="创建时间">{{ item.create_datetime }}</el-descriptions-item>
                </el-descriptions>
              </div>
            </el-popover>
            <el-popconfirm title="您确定要删除?" @confirm="onDel(item)">
              <template #reference>
                <el-button type="text">删除</el-button>
              </template>
            </el-popconfirm>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-divider></el-divider>
    <el-row style="margin-left: 10px">
      <el-col :span="12" >
        <el-pagination
            v-model:current-page="pageConfig.page"
            v-model:page-size="pageConfig.limit"
            background
            :page-sizes="[5, 10, 20, 50]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="pageConfig.total"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
        />
      </el-col>
    </el-row>
  </fs-page>
</template>

<script lang="ts" setup name="fileList">
import {DelObj, GetList} from "./api";
import {ref, onMounted,reactive} from "vue";
import {getBaseURL} from "/@/utils/baseUrl";
import {ElMessage} from "element-plus";
import { Delete, Edit, Search, Share, Upload } from '@element-plus/icons-vue'
const fileParams = reactive({name:''})
const fileList = ref([])
const mimeType = ref([])
const pageConfig = reactive({
  page:1,
  limit:10,
  total:0
})
const getData = function () {
  let params = {
    page:pageConfig.page,
    limit:pageConfig.limit,
    name:fileParams.name
  }
  GetList(params).then((res: any) => {
    const {data,page,limit,total} = res
    pageConfig.page = page
    pageConfig.limit=limit
    pageConfig.total=total
    fileList.value = data
  })
}


const onDel = function (item: any) {
  DelObj(item.id).then((res: any) => {
    ElMessage.success("删除成功！");
    getData()
  })
}
const formatImgUrl = function (src: string) {
  return getBaseURL() + src
}

const handleSizeChange = function (val: any) {
  pageConfig.limit = val
  getData()
}

const handleCurrentChange = function (val: any) {
  pageConfig.page = val
  getData()
}

onMounted(() => {
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

.el-tabs__nav-scroll {
  border-right: 1px solid #efefef;
}
</style>
