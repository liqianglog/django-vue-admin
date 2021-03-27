<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="系统模块" prop="request_modular">
        <el-input
          v-model="queryParams.request_modular"
          placeholder="请输入系统模块"
          clearable
          style="width: 240px;"
          size="small"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="操作人员" prop="creator_name">
        <el-input
          v-model="queryParams.creator_name"
          placeholder="请输入操作人员"
          clearable
          style="width: 240px;"
          size="small"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-select
          v-model="queryParams.status"
          placeholder="操作状态"
          clearable
          size="small"
          style="width: 240px"
        >
          <el-option
            v-for="dict in statusOptions"
            :key="dict.dictValue"
            :label="dict.dictLabel"
            :value="dict.dictValue"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="操作时间">
        <el-date-picker
          v-model="dateRange"
          size="small"
          style="width: 240px"
          value-format="yyyy-MM-dd HH:mm:ss"
          type="daterange"
          range-separator="-"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          :default-time="['00:00:00', '23:59:59']"
        ></el-date-picker>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="el-icon-delete"
          size="mini"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['admin:system:operation_log:{id}:delete']"
        >删除
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="el-icon-delete"
          size="mini"
          @click="handleClean"
          v-hasPermi="['admin:system:operation_log:clean:delete']"
        >清空
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="el-icon-download"
          size="mini"
          @click="handleExport"
          v-hasPermi="['admin:system:operlog:export:get']"
        >导出
        </el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="list" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center"/>
      <el-table-column label="日志编号" align="center" prop="id"/>
      <el-table-column label="系统模块" align="center" prop="request_modular"/>
      <el-table-column label="请求方式" align="center" prop="request_method"/>
      <el-table-column label="操作人员" align="center" prop="creator_name"/>
      <el-table-column label="主机" align="center" prop="request_ip" width="130" :show-overflow-tooltip="true"/>
      <el-table-column label="操作地点" align="center" prop="request_location" :show-overflow-tooltip="true"/>
      <el-table-column label="操作状态" align="center" prop="status" :formatter="statusFormat"/>
      <el-table-column label="操作日期" align="center" prop="create_datetime" width="180">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.create_datetime) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-view"
            @click="handleView(scope.row,scope.index)"
            v-hasPermi="['admin:system:operlog:get']"
          >详细
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="queryParams.pageNum"
      :limit.sync="queryParams.pageSize"
      @pagination="getList"
    />

    <!-- 操作日志详细 -->
    <!-- 表单类详情dialog-->
    <detail-form-dialog v-if="openDetailModal"
                        dialog-title="操作日志详细"
                        modalWidth="700px"
                        :openDetailModal="openDetailModal"
                        :formData="form"
                        :formItem="formItem"
                        @closeDialog="value=>{openDetailModal=value}"
    >
      <template slot="customRequestModular" slot-scope="{item}">
        <span>{{connectFieldsContent([form.request_modular, form.request_msg], '/') }}</span>
      </template>
      <template slot="customLoginInfo" slot-scope="{item}">
        <span>{{connectFieldsContent([form.creator_name, form.request_ip, form.request_location, form.request_browser], '/')}}</span>
      </template>
    </detail-form-dialog>
  </div>
</template>

<script>
  import { cleanOperationLog, delOperationLog, exportOperationLog, list } from '@/api/vadmin/system/operationlog'
  import DetailFormDialog from '@/components/Modal/DetailFormDialog'
  import log from '../job/log'

  const OPERATION_LOG_FORM_ITEM = [
    {
      index: 1,
      label: '操作模块',
      key: 'customRequestModular',
      customRender: true,
      singleLine: true
    },
    {
      index: 2,
      label: '登录信息',
      key: 'customLoginInfo',
      customRender: true,
      singleLine: true
    },
    {
      index: 3,
      label: '请求地址',
      key: 'request_path'
    },
    {
      index: 4,
      label: '请求参数',
      key: 'request_body',
      singleLine: true
    },
    {
      index: 5,
      label: '返回参数',
      key: 'json_result'
    },
    {
      index: 6,
      label: '返回状态码',
      key: 'response_code'
    },
    {
      index: 7,
      label: '操作状态',
      key: 'status',
      labelType: 'boolean',
      labelChoices: {
        false: '失败',
        true: '正常'
      }
    },
    {
      index: 8,
      label: '任务结果',
      key: 'result',
      singleLine: true
    },
    {
      index: 9,
      label: '操作时间',
      key: 'create_datetime',
      labelType: 'time',
      singleLine: true
    }
  ]

  export default {
    name: 'Operlog',
    components: { DetailFormDialog },
    data() {
      return {
        // 遮罩层
        loading: true,
        // 选中数组
        ids: [],
        // 非多个禁用
        multiple: true,
        // 显示搜索条件
        showSearch: true,
        // 总条数
        total: 0,
        // 表格数据
        list: [],
        // 是否显示弹出层
        openDetailModal: false,
        // 类型数据字典
        statusOptions: [{ dictLabel: '成功', dictValue: true }, { dictLabel: '失败', dictValue: false }],
        // 日期范围
        dateRange: [],
        // 表单参数
        form: {},
        formItem: OPERATION_LOG_FORM_ITEM,
        // 查询参数
        queryParams: {
          pageNum: 1,
          pageSize: 10,
          request_modular: undefined,
          creator_name: undefined,
          status: undefined
        }
      }
    },
    created() {
      this.getList()
    },
    methods: {
      /** 查询登录日志 */
      getList() {
        this.loading = true
        list(this.addDateRange(this.queryParams, this.dateRange)).then(response => {
            this.list = response.data.results
            this.total = response.data.count
            this.loading = false
          }
        )
      },
      // 操作日志状态字典翻译
      statusFormat(row, column) {
        return this.selectDictLabel(this.statusOptions, row.status)
      },
      /** 搜索按钮操作 */
      handleQuery() {
        this.queryParams.pageNum = 1
        this.getList()
      },
      /** 重置按钮操作 */
      resetQuery() {
        this.dateRange = []
        this.resetForm('queryForm')
        this.handleQuery()
      },
      // 多选框选中数据
      handleSelectionChange(selection) {
        this.ids = selection.map(item => item.id)
        this.multiple = !selection.length
      },
      /** 详细按钮操作 */
      handleView(row) {
        this.openDetailModal = true
        this.form = row
      },
      /** 删除按钮操作 */
      handleDelete(row) {
        const ids = row.id || this.ids
        this.$confirm('是否确认删除日志编号为"' + ids + '"的数据项?', '警告', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(function() {
          return delOperationLog(ids)
        }).then(() => {
          this.getList()
          this.msgSuccess('删除成功')
        })
      },
      /** 清空按钮操作 */
      handleClean() {
        this.$confirm('是否确认清空所有操作日志数据项?', '警告', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(function() {
          return cleanOperationLog()
        }).then(() => {
          this.getList()
          this.msgSuccess('清空成功')
        })
      },
      /** 导出按钮操作 */
      handleExport() {
        const queryParams = this.queryParams
        this.$confirm('是否确认导出所有操作日志数据项?', '警告', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(function() {
          return exportOperationLog(queryParams)
        }).then(response => {
          this.download(response.data.file_url, response.data.name)
        })
      },
      connectFieldsContent(fieldsContent, symbol) {
        fieldsContent.forEach((fieldContent, index) => {
          if (!fieldContent) {
            delete fieldsContent[index]
          }
        })
        return fieldsContent.join(symbol)
      }
    }
  }
</script>

