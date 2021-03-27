<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="任务名称" prop="name">
        <el-input
          v-model="queryParams.name"
          placeholder="请输入任务名称"
          clearable
          style="width: 240px;"
          size="small"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="函数名称" prop="func_name">
        <el-input
          v-model="queryParams.func_name"
          placeholder="请输入执行函数名称"
          clearable
          style="width: 240px;"
          size="small"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-select
          v-model="queryParams.status"
          placeholder="运行状态"
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
      <el-form-item label="执行时间">
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
          v-hasPermi="['admin:system:celery_log:{id}:delete']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="el-icon-delete"
          size="mini"
          @click="handleClean"
          v-hasPermi="['admin:system:celery_log:clean:delete']"
        >清空</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="el-icon-download"
          size="mini"
          @click="handleExport"
          v-hasPermi="['admin:system:celery_log:export:get']"
        >导出</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="list" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="日志编号" width="80" align="center" prop="id" />
      <el-table-column label="任务名称" align="center" prop="name" width="200" :show-overflow-tooltip="true" />
      <el-table-column label="执行函数名称" align="center" prop="func_name" :show-overflow-tooltip="true" />
      <el-table-column label="执行参数" align="center" prop="kwargs" :show-overflow-tooltip="true" />
      <el-table-column label="执行时间" width="80" align="center" prop="seconds" />
      <el-table-column label="运行状态" width="80" align="center" prop="status" :formatter="statusFormat"/>
      <el-table-column label="任务结果" align="center" prop="result" :show-overflow-tooltip="true" />
      <el-table-column label="执行日期" align="center" prop="create_datetime" width="180">
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
            v-hasPermi="['admin:system:celerylog:get']"
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

    <!-- 表单类详情dialog-->
    <detail-form-dialog v-if="openDetailModal"
                        dialog-title="定时日志详细"
                        modalWidth="700px"
                        :openDetailModal="openDetailModal"
                        :formData="form"
                        :formItem="formItem"
                        @closeDialog="value=>{openDetailModal=value}"
    ></detail-form-dialog>
  </div>
</template>

<script>
import { list, delCeleryLog, cleanCeleryLog, exportCeleryLog } from "@/api/vadmin/monitor/celery";
import DetailFormDialog from '@/components/Modal/DetailFormDialog'

const CELERY_LOG_FORM_ITEM = [
  {
    index: 1,
    label: '日志编号',
    key: 'id'
  },
  {
    index: 2,
    label: '任务名称',
    key: 'name'
  },
  {
    index: 3,
    label: '执行函数名称',
    key: 'func_name',
    width: "auto"
  },
  {
    index: 4,
    label: '执行参数',
    key: 'kwargs',
    singleLine: true
  },
  {
    index: 5,
    label: '执行时间',
    key: 'seconds'
  },
  {
    index: 6,
    label: '运行状态',
    key: 'status',
    labelType: 'boolean',
    labelChoices: {
      false: '失败',
      true: '正常'
    }
  },
  {
    index: 7,
    label: '任务结果',
    key: 'result',
    singleLine: true
  },
  {
    index: 8,
    label: '执行日期',
    key: 'create_datetime',
    labelType: 'time',
    singleLine: true
  }
];

export default {
  name: "CeleryLog",
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
      // 是否显示详细模态框
      openDetailModal: false,
      list: [],
      // 状态数据字典
      statusOptions:[{dictLabel: '成功', dictValue: true}, {dictLabel: '失败', dictValue: false}],
      // 日期范围
      dateRange: [],
      form: {},
      formItem: CELERY_LOG_FORM_ITEM,

      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        name: undefined,
        func_name: undefined,
        status: undefined
      }
    };
  },
  created() {
    this.getList();
    // this.getDicts("sys_common_status").then(response => {
    //   this.statusOptions = response.data;
    // });
  },
  methods: {

    /** 查询登录日志列表 */
    getList() {
      this.loading = true;
      list(this.addDateRange(this.queryParams, this.dateRange)).then(response => {
          this.list = response.data.results;
          this.total = response.data.count;
          this.loading = false;
        }
      );
    },
    // 运行状态字典翻译
    statusFormat(row, column) {
      return this.selectDictLabel(this.statusOptions, row.status);
    },
    /** 搜索按钮操作 */
    handleQuery() {
      this.queryParams.pageNum = 1;
      console.log(this.queryParams)
      this.getList();
    },
    /** 重置按钮操作 */
    resetQuery() {
      this.dateRange = [];
      this.resetForm("queryForm");
      this.handleQuery();
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
      const infoIds = row.id || this.ids;
      this.$confirm('是否确认删除访问编号为"' + infoIds + '"的数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function() {
          return delCeleryLog(infoIds);
        }).then(() => {
          this.getList();
          this.msgSuccess("删除成功");
        })
    },
    /** 清空按钮操作 */
    handleClean() {
        this.$confirm('是否确认清空所有登录日志数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function() {
          return cleanCeleryLog();
        }).then(() => {
          this.getList();
          this.msgSuccess("清空成功");
        })
    },
    /** 导出按钮操作 */
    handleExport() {
      const queryParams = this.queryParams;
      this.$confirm('是否确认导出所有定时日志数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function() {
          return exportCeleryLog(queryParams);
        }).then(response => {
          this.download(response.data.file_url,response.data.name);
        })
    }
  }
};
</script>

