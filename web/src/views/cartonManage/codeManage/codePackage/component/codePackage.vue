<!--
 * @创建文件时间: 2021-11-25 10:34:46
 * @Auther: 猿小天
 * @最后修改人: 猿小天
 * @最后修改时间: 2021-12-22 21:53:20
 * 联系Qq:1638245306
 * @文件介绍:
-->
<template>
  <el-container>
    <el-main>
      <div>
        <el-table
          :data="tableData"
          border
          height="500"
          style="width: 100%"
          row-key="id"
          :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
        >
          <el-table-column prop="id" label="码包编号"> </el-table-column>
          <el-table-column prop="code_number" label="码包内码总数" width="200">
          </el-table-column>
          <el-table-column prop="package_no" label="拆包编号" width="120">
          </el-table-column>
          <el-table-column prop="code_package_status_label" label="码包状态" width="120">
            <template slot-scope="{ row }">
              <el-tag type="primary" v-if="[1,4].indexOf(row.status)>-1">{{ row.code_package_status_label}}</el-tag>
              <el-tag type="warning" v-else-if="[5].indexOf(row.status)>-1">{{ row.code_package_status_label}}</el-tag>
              <el-tag type="success" v-else-if="[6].indexOf(row.status)>-1">{{ row.code_package_status_label}}</el-tag>
              <el-tag type="error" v-else-if="[7].indexOf(row.status)>-1">{{ row.code_package_status_label}}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="update_datetime" label="最后修改时间">
          </el-table-column>
        </el-table>
      </div>
    </el-main>
  </el-container>
</template>
<script>
import * as api from '../api'
import XEUtils from 'xe-utils'
export default {
  props: {
    options: {
      type: Object,
      default () {
        return {}
      }
    }
  },
  data () {
    return {
      tableData: []
    }
  },
  methods: {
    getList () {
      if (this.options.mainId) {
        const params = {
          limit: 999,
          brand_owner_order: this.options.mainId
        }
        api.getCodePackage(params).then((res) => {
          const { data } = res.data
          this.tableData = XEUtils.toArrayTree(data, {
            parentKey: 'parent'
          })
        })
      }
    }
  },
  created () {
    this.getList()
  }
}
</script>
