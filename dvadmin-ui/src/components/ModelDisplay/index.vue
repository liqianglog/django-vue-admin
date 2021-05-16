<!--
@description: 强大的CRUD组件封装
-->
<template>
  <div style="padding-left: 10px;padding-top: 10px;">
    <div class="grid-content bg-purple">
      <el-form :model="queryParams" ref="queryForm" :inline="true" label-width="90px">
        <el-row>
          <el-form-item v-if="value.search" :label="value.label" :prop="value.prop" v-for="(value,index) in fields"
                        :key="index">
            <!--           date/option/bool/users/depts -->
            <el-switch
              v-if="value.type==='boolean'"
              v-model="queryParams[value.prop]"
              active-color="#13ce66"
              inactive-color="#ff4949">
            </el-switch>
            <dept-tree ref="dept_tree" v-else-if="value.type==='depts'" :value.sync="queryParams[value.prop]"
                       style="width: 150px;"></dept-tree>
            <users-tree ref="users_tree" v-else-if="value.type==='users'" :value.sync="queryParams[value.prop]"
                        style="width: 150px;"></users-tree>
            <el-date-picker
              v-else-if="value.type==='date'"
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
            <el-select
              v-else-if="value.type==='option' && value.option_key"
              v-model="queryParams[value.prop]"
              :placeholder="value.label"
              clearable
              size="small"
              style="width: 240px"
            >
              <el-option
                v-for="dict in DictsOptions[value.option_key]"
                :key="dict.dictValue"
                :label="dict.dictLabel"
                :value="dict.dictValue"
              />
            </el-select>
            <el-input
              v-else
              v-model="queryParams[value.prop]"
              :placeholder="value.label"
              clearable
              size="small"
              @keyup.enter.native="handleQuery"
            />
          </el-form-item>
        </el-row>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" size="mini" @click="handleSearchFormSubmit">搜索</el-button>
          <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
    <el-row v-if="topLayout" style="margin-bottom: 20px">
      <el-col v-if="topLayoutLeft" :span="18">
        <el-row :gutter="10" class="mb8">
          <el-col :span="1.5" v-for="(func,index) in funcs" :key="index">
            <el-button
              v-if="func.type==='add'"
              type="primary"
              plain
              :icon="func.icon||'el-icon-plus'"
              size="mini"
              @click="handleAdd(func.api)"
              v-hasPermi="func.permis"
            >{{func.label}}
            </el-button>
            <el-button
              v-else-if="func.type==='update'"
              type="success"
              plain
              :disabled="multipleSelection.length!==1"
              :icon="func.icon||'el-icon-edit'"
              size="mini"
              @click="handleUpdate(func.api,{})"
              v-hasPermi="func.permis"
            >{{func.label}}
            </el-button>
            <el-button
              v-else-if="func.type==='delete'"
              type="danger"
              plain
              :disabled="multipleSelection.length===0"
              :icon="func.icon||'el-icon-delete'"
              size="mini"
              @click="handleDelete(func.api,{})"
              v-hasPermi="func.permis"
            >{{func.label}}
            </el-button>
            <el-button
              v-else-if="func.type==='export'"
              type="warning"
              plain
              :icon="func.icon||'el-icon-download'"
              size="mini"
              @click="handleExport(func.api)"
              v-hasPermi="func.permis"
            >{{func.label}}
            </el-button>
            <el-button
              v-else-if="func.type==='import'"
              type="info"
              plain
              :icon="func.icon||'el-icon-upload2'"
              size="mini"
              @click="handleImport(func.api)"
              v-hasPermi="func.permis"
            >{{func.label}}
            </el-button>
          </el-col>
        </el-row>
      </el-col>
      <el-col v-if="topLayoutRight" :span="6">
        <div class="grid-content bg-purple-light" style="text-align: right">
          <slot name="tools"/>
          <el-popover
            placement="bottom"
            width="200"
            trigger="click">
            <div style="width: 50px;">
              <el-checkbox-group v-model="showFields">
                <el-checkbox v-for="(field, index) in fields" :key="index" :label="field" :checked="field.show"
                             style="width: 100%" @change="handleSelectField($event, field)">{{ field.label }}
                </el-checkbox>
              </el-checkbox-group>
            </div>
            <el-button
              slot="reference"
              :size="$ELEMENT.size"
              name="refresh"
              type="info"
              icon="el-icon-s-fold"
              title="设置显示的字段"/>
          </el-popover>
        </div>
      </el-col>
    </el-row>

    <el-table
      v-loading="tableLoading"
      ref="tableData"
      :span-method="spanMethod"
      :data="tableData"
      :max-height="maxHeight"
      :row-key="getRowKeys"
      :stripe="stripe"
      :fit="fit"
      :border="border"
      :empty-text="emptyText"
      :highlight-current-row="highlightCurrentRow"
      :show-overflow-tooltip="showOverflowTooltip"
      @sort-change="handleSortChange"
      @cell-click="handleCellClick"
      @cell-dblclick="handleCellDbClick"
      @header-click="handleHeaderClick"
      @row-click="handleRowClick"
      @row-dblclick="handleRowDblClick"
      @selection-change="handleSelectionChange">
      <el-table-column v-if="selection" :reserve-selection="true" type="selection" width="50"/>
      <slot name="prependColumn"/>
      <!--<el-table-column v-if="false" :index="getRowIndex" label="序号" type="index" width="50"/>-->
      <template v-for="field in fields">
        <el-table-column
          v-if="field.show"
          :key="field.prop"
          :prop="field.prop"
          :label="field.label"
          :sortable="field.sortable"
          :width="field.width || ''"
          :sort-method="sortMethod"
          show-overflow-tooltip>
          <template slot-scope="scope">
            <slot :name="field.prop" :values="scope.row" :prop="field.prop" :field="field">
              <span v-html="formatColumnData(scope.row, field)"/>
            </slot>
          </template>
        </el-table-column>
      </template>
      <el-table-column
        label="操作"
        align="center"
        class-name="small-padding fixed-width"
        v-if="hasPermi(getOperationPermis())"
      >
        <template slot-scope="scope">
          <span v-for="(func,index) in funcs" :key="index">
            <el-button
              v-if="func.type==='select'"
              size="mini"
              type="text"
              :icon="func.icon||'el-icon-view'"
              @click="handleSelect(func.api,scope.row)"
              v-hasPermi="func.permis"
            >{{func.label}}</el-button>
            &nbsp;
            <el-button
              v-if="func.type==='update'"
              size="mini"
              type="text"
              :icon="func.icon||'el-icon-edit'"
              @click="handleUpdate(func.api,scope.row)"
              v-hasPermi="func.permis"
            >{{func.label}}</el-button>
            &nbsp;
            <el-button
              v-else-if="func.type==='delete'"
              size="mini"
              type="text"
              :icon="func.icon||'el-icon-delete'"
              @click="handleDelete(func.api,scope.row)"
              v-hasPermi="func.permis"
            >{{func.label}}</el-button>
          </span>
        </template>
      </el-table-column>
      <slot name="appendColumn"/>
      <slot name="column"/>
    </el-table>
    <el-row>
      <el-col v-if="selection" :span="6" style="margin-top: 20px">
        <span>已选择:<span style="color: #ff00ff;font-weight: bold;">{{ multipleSelection.length }}</span>条</span>
        <el-button v-show="multipleSelection.length" type="info" size="mini" title="清空多选"
                   @click="clearMultipleSelection">清空
        </el-button>
      </el-col>
      <el-pagination
        :current-page="pagination.page"
        :page-size="pagination.page_size"
        :total="pagination.total"
        :page-sizes="paginationStyle.pageSizes || [10, 20, 50, 100]"
        :disabled="tableLoading"
        :small="paginationStyle.small || false"
        :layout="paginationStyle.layout || 'total, sizes, prev, pager, next, jumper'"
        background
        class="right_pagination"
        @size-change="handleChangePageSize"
        @current-change="handleChangeCurrentPage"/>
    </el-row>

    <!-- 添加或修改参数配置对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="100px">
        <el-form-item v-if="value.form" :label="value.label" :prop="value.prop" v-for="(value,index) in fields"
                      :key="index">
          <!--           date/option/bool/users/depts -->
          <el-switch
            v-if="value.type==='boolean'"
            v-model="form[value.prop]"
            active-color="#13ce66"
            inactive-color="#ff4949">
          </el-switch>
          <dept-tree ref="dept_tree" v-else-if="value.type==='depts'" :value.sync="form[value.prop]"
                     style="width: 200px;"></dept-tree>
          <users-tree ref="users_tree" v-else-if="value.type==='users'" :value.sync="form[value.prop]"
                      style="width: 200px;"></users-tree>
          <el-date-picker
            v-else-if="value.type==='date'"
            v-model="form[value.prop]"
            type="date"
            size="small"
            style="width: 240px"
            value-format="yyyy-MM-dd HH:mm:ss"
            placeholder="选择日期">
          </el-date-picker>
          <el-select
            v-else-if="value.type==='option' && value.option_key"
            v-model="form[value.prop]"
            :placeholder="value.label"
            clearable
            size="small"
            style="width: 240px"
          >
            <el-option
              v-for="dict in DictsOptions[value.option_key]"
              :key="dict.dictValue"
              :label="dict.dictLabel"
              :value="dict.dictValue"
            />
          </el-select>
          <el-input
            v-else
            v-model="form[value.prop]"
            :placeholder="value.label"
            clearable
            size="small"
          />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm" v-if="this.title!=='详情'">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>
    <!-- 导入对话框 -->
    <el-dialog :title="upload.title" :visible.sync="upload.open" width="400px" append-to-body>
      <el-upload
        ref="upload"
        :limit="1"
        accept=".xlsx, .xls"
        :headers="upload.headers"
        :action="upload.url + '?updateSupport=' + upload.updateSupport"
        :disabled="upload.isUploading"
        :on-progress="handleFileUploadProgress"
        :on-success="handleFileSuccess"
        :auto-upload="false"
        drag
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">
          将文件拖到此处，或
          <em>点击上传</em>
        </div>
        <div class="el-upload__tip" slot="tip">
          <el-checkbox v-model="upload.updateSupport"/>
          是否更新已经存在的数据
          <el-link type="info" style="font-size:12px" @click="importTemplate">下载模板</el-link>
        </div>
        <div class="el-upload__tip" style="color:red" slot="tip">提示：仅允许导入“xls”或“xlsx”格式文件！</div>
      </el-upload>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitFileForm">确 定</el-button>
        <el-button @click="upload.open = false">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
  import moment from 'moment';
  import * as Utils from '@/utils';
  import {getToken} from '@/utils/auth'

  export default {
    name: 'ModelDisplay',
    props: {
      value: {
        // table的Data
        type: Array,
        default: () => []
      },
      spanMethod: {
        type: Function,
        default: null
      },
      // eslint-disable-next-line vue/require-prop-types
      maxHeight: {
        default: 700
      },
      stripe: {
        type: Boolean,
        default: true
      },
      fit: {
        type: Boolean,
        default: true
      },
      highlightCurrentRow: {
        type: Boolean,
        default: true
      },
      showOverflowTooltip: {
        type: Boolean,
        default: true
      },
      border: {
        type: Boolean,
        default: false
      },
      emptyText: {
        type: String,
        default: '暂无数据'
      },
      paginationParams: {
        // 新增。分页参数, 当分页格式返回的属性名称不同使用, 可使用该属性覆盖默认分页属性名称
        // 例如:{ page: 'page', pageSize: 'pageSize', count: 'total',results: 'list' }
        type: Object,
        default: () => {
          return {
            page: 'page',
            pageSize: 'page_size',
            count: 'count',
            results: 'results'
          };
        }
      },
      listApi: {
        // 用于替换method + url属性
        type: Function,
        default: null
      },
      topLayout: {
        // 用于控制表格顶部的按钮、工具的显示。默认左右的按钮、功能都显示
        type: Array,
        default: () => {
          return ['left', 'right'];
        }
      },
      fields: {
        // 后端返回的字段
        type: Array,
        default: () => {
          return [];
        }
      },
      funcs: {
        // 菜单配置字段
        type: Array,
        default: () => {
          return [];
        }
      },
      selection: {
        // 开始开启多选(默认开启, true)
        type: Boolean,
        default: true
      },
      params: {
        // 基本请求参数,最终请求参数=基本参数+基本高级搜索参数+组件封装的基本参数+租金组件封装的高级搜索参数
        type: Object,
        default: () => {
          return {};
        }
      },
      // 默认分页样式
      paginationStyle: {
        type: Object,
        default: () => {
          return {};
        }
      },
      // 默认页面大小
      pageSizes: {
        type: Array,
        default: () => {
          return [10, 20, 50, 100, 500];
        }
      }
    },
    data() {
      return {
        showFields: [], // 显示的字段
        searchForm: {
          search: '',
          ordering: ''
        },
        queryParams: {},
        tableLoading: false,
        tableData: [],
        rowKey: '',
        dateRange: [],
        multipleSelection: [],
        pagination: {
          page: 1,
          page_size: 10,
          total: 0
        },
        // 表单参数
        form: {},
        rules: this.getFormRules(),
        open: false,
        // 提交时api
        submitFormApi: '',
        // 单个查询api
        selectApi: '',
        // 导入api
        importApi: '',
        DictsOptions: {},
        getRowKeys: row => {
          if (this.rowKey) {
            return row[this.rowKey];
          }
          return row.id || row.uuid;
        },
        title: '',
        // 用户导入参数
        upload: {
          // 是否显示弹出层（用户导入）
          open: false,
          // 弹出层标题（用户导入）
          title: '',
          // 是否禁用上传
          isUploading: false,
          // 是否更新已经存在的用户数据
          updateSupport: 0,
          // 设置上传的请求头部
          headers: {Authorization: 'Bearer ' + getToken()},
          // 上传的地址
          url: process.env.VUE_APP_BASE_API + '/admin/system/savefile/'
        },
      };
    },
    computed: {
      topLayoutLeft() {
        return this.topLayout.indexOf('left') >= 0;
      },
      topLayoutRight() {
        return this.topLayout.indexOf('right') >= 0;
      },
    },
    watch: {
      params: {
        deep: true,
        handler: function (newValue, oldValue) {
          this.getTableData();
        }
      },
    },
    mounted() {
    },
    created() {
      this.initComponentData();
      this.initDictsOptions();
      this.getTableData();
      this.funcs.map(value => {
        if (value.type === 'select') {
          this.selectApi = value.api
        }
      })
    },
    methods: {
      initComponentData() {
        this.pagination.page_size = this.pageSizes[0];
        this.fields.forEach(field => {
          field.show = (!!field.show);
          field.type = (field.type || 'string').toLocaleLowerCase();
          if (field.type.startsWith('bool')) {
            field.type = 'boolean';
          }
          field.label = field.label || field.prop;
          field.search = (!!field.search);
          field.sortable = (!!field.sortable);
          if (field.ordering && field.ordering.startsWith('desc')) {
            this.searchForm.ordering = `-${field.prop}`;
          } else if (field.ordering && field.ordering.startsWith('asc')) {
            this.searchForm.ordering = `${field.prop}`;
          }
          field.width = field.width || '';
          if (field.type === 'choices') {
            if (Utils.isArray(field.choices) && field.choices.length > 0) {
              if (!Utils.isObj(field.choices[0])) {
                field.choices = field.choices.map(value => {
                  return {
                    label: value,
                    value: value
                  };
                });
              }
            }
          }
          field.unique = (!!field.unique);
          if (field.unique) {
            this.rowKey = field.prop;
          }
        });
      },
      formatColumnData(row, field) {
        const type = field.type || 'string';
        const prop = field.prop;
        if (field.formatter && typeof field.formatter === 'function') {
          return field.formatter(row, prop, type);
        }
        if (type === 'string') {
          return row[prop];
        } else if (type === 'datetime') {
          return this.formatDatetime(row[prop]);
        } else if (type === 'date') {
          return this.formatDate(row[prop]);
        } else if (type === 'time') {
          return this.formatTime(row[prop]);
        } else if (type === 'option') {
          return this.formatOptions(field.option_key, row[prop]);
        } else if (type === 'users') {
          return this.formatUsers(row[prop]);
        } else if (type === 'depts') {
          return this.formatDepts(row[prop]);
        } else if (type.startsWith('bool')) {
          return row[prop] ? '是' : '否';
        } else if (type === 'choices') {
          const choices = field.choices;
          return this.formatChoices(choices, row[prop]);
        } else {
          return row[prop];
        }
      },
      formatChoices(choices, value) {
        for (const choice of choices) {
          if (choice.value === value) {
            return choice.label;
          }
        }
        return value;
      },
      formatDatetime(datetime) {
        return moment(datetime).format('YYYY-MM-DD HH:mm:ss');
      },
      formatDate(date) {
        return moment(date).format('YYYY-MM-DD');
      },
      formatTime(time) {
        return moment(time).format('HH:mm:ss');
      },
      formatOptions(option_key, id) {
        var data = this.DictsOptions[option_key]
        if (!id || !data) return ""
        for (var i = 0; i < data.length; i++) {
          if (data[i].dictValue === id) {
            return data[i].dictLabel
          }
        }
        return ""
      },
      formatUsers(id) {
        if (!id) return ""
        var data = this.$refs.users_tree[0].usersOptions
        for (var i = 0; i < data.length; i++) {
          if (data[i].id === id) {
            return data[i].label
          }
        }
        return ""
      },
      formatDepts(id) {
        if (!id) return ""
        var data = this.$refs.dept_tree[0].deptOptions
        for (var i = 0; i < data.length; i++) {
          if (data[i].id === id) {
            return data[i].label
          }
        }
        return ""
      },
      sortMethod(a, b) {
        return -1;
      },
      getTableData() {
        this.listInterfaceData(this.getRequestParams());
        return this.tableData;
      },
      getFormattedPaginationParams() {
        const pageParamName = this.paginationParams.page;
        const pageSizeParamName = this.paginationParams.pageSize;
        const params = {};
        params[pageParamName] = this.pagination.page;
        params[pageSizeParamName] = this.pagination.page_size;
        return params;
      },
      // 根据搜索框的内容, 组装请求参数
      getRequestParams() {
        // 组装分页参数、高级搜索参数
        const tmpParams = {...this.params, ...this.getFormattedPaginationParams(), ...this.queryParams};
        const params = {};
        for (const prop of Object.keys(tmpParams)) {
          if (tmpParams[prop]) {
            params[prop] = tmpParams[prop];
          }
        }
        // 组装普遍模糊搜索的参数
        if (this.searchForm.search) {
          params['search'] = this.searchForm.search;
        }
        // 组装普遍排序搜索的参数
        if (this.searchForm.ordering) {
          params['ordering'] = this.searchForm.ordering;
        }
        // console.dir(params);
        return this.addDateRange(params, this.dateRange);
      },
      // 封装后端接口, 后端接口返回数据必须规范一致
      listInterfaceData(params) {
        this.tableLoading = true;
        this.listApi(params).then(response => {
          this.tableLoading = false;
          if (response.status === 'success') {
            const resultsParamName = this.paginationParams.results;
            const countParamName = this.paginationParams.count;
            this.tableData = response.data[resultsParamName] || [];
            this.pagination.total = response.data[countParamName] || 0;
          } else {
            this.$message.warning(response.msg || '获取接口信息失败!');
          }
        }).catch(error => {
          this.tableLoading = false;
          console.error(error);
        });
      },
      /** 清空已选择 */
      clearMultipleSelection() {
        this.clearSelection();
      },
      /** 清空已选择 */
      clearSelection() {
        this.$refs.tableData.clearSelection();
      },
      handleSelectField(e, field) {
        field.show = e;
      },
      // 处理提交表单, 点击搜索按钮事件
      handleSearchFormSubmit() {
        this.pagination.page = 1;
        this.getTableData();
      },
      /** 搜索按钮操作 */
      handleQuery() {
        this.queryParams.pageNum = 1;
        this.getTableData();
      },
      /** 重置按钮操作 */
      resetQuery() {
        this.dateRange = [];
        this.queryParams = {}
        this.resetForm("queryForm");
        this.handleQuery();
      },
      /** 获取Dicts值 */
      initDictsOptions() {
        this.fields.map(value => {
          if (value.option_key) {
            this.getDicts(value.option_key).then(response => {
              this.DictsOptions[value.option_key] = response.data
            })
          }
        })
      },
      // 处理修改多选的值
      handleSelectionChange(val) {
        this.$emit('selection-change', val);
        this.multipleSelection = val;
      },
      // 处理修改表格分页器的页面大小(再次获取接口数据)
      handleChangePageSize(val) {
        this.pagination.page_size = val;
        this.getTableData();
      },
      // 处理修改表格分页器的页码(再次获取接口数据)
      handleChangeCurrentPage(val) {
        this.pagination.page = val;
        this.getTableData();
      },
      handleSortChange(info) {
        const {prop, order} = info;
        if (!order) {
          this.searchForm.ordering = '';
        } else if (order.startsWith('desc')) {
          this.searchForm.ordering = `-${prop}`;
        } else {
          this.searchForm.ordering = `${prop}`;
        }
        this.getTableData();
      },
      handleCellClick(row, column, cell, event) {
        this.$emit('cell-click', row, column, cell, event);
      },
      handleCellDbClick(row, column, cell, event) {
        this.$emit('cell-dblclick', row, column, cell, event);
      },
      handleRowClick(row, column, event) {
        this.$emit('row-click', row, column, event);
      },
      handleRowDblClick(row, column, event) {
        this.$emit('row-dblclick', row, column, event);
      },
      handleHeaderClick(column, event) {
        this.$emit('header-click', column, event);
      },
      /**新增按钮*/
      handleAdd(api) {
        this.dateRange = [];
        this.queryParams = {}
        this.resetForm("queryForm");
        this.open = true;
        this.title = "新增";
        this.submitFormApi = api

      },
      /**修改按钮*/
      handleUpdate(api, row) {
        this.dateRange = [];
        this.queryParams = {}
        this.resetForm("queryForm");
        this.submitFormApi = api
        const id = row.id || this.multipleSelection.map(item => item.id);
        if (this.selectApi) {
          this.selectApi(id).then(response => {
            this.form = response.data;
            this.open = true;
            this.title = "修改";
          });
        } else {
          this.open = true;
          this.title = "修改";
        }
      },
      /**修改按钮*/
      handleSelect(api, row) {
        this.dateRange = [];
        this.queryParams = {}
        this.resetForm("queryForm");
        this.submitFormApi = api
        const id = row.id || this.multipleSelection.map(item => item.id);
        if (this.selectApi) {
          this.selectApi(id).then(response => {
            this.form = response.data;
            this.open = true;
            this.title = "详情";
          });
        } else {
          this.open = true;
          this.title = "详情";
        }
      },
      /** 删除按钮操作 */
      handleDelete(api, row) {
        const ids = row.id || this.multipleSelection.map(item => item.id);
        this.$confirm('是否确认删除编号为"' + ids + '"的数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function () {
          return api(ids);
        }).then(() => {
          this.getTableData();
          this.msgSuccess("删除成功");
        })
      },
      /** 导出按钮操作 */
      handleExport(api) {
        const queryParams = this.queryParams;
        this.$confirm('是否确认导出所有符合条件的数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function () {
          return api(queryParams);
        }).then(response => {
          this.download(response.data.file_url, response.data.name);
        })
      },
      /** 导入按钮操作 */
      handleImport() {
        this.upload.title = '导入'
        this.upload.open = true
      }, /** 获取表单校验 */
      getFormRules() {
        let dict = {}
        this.fields.map(value => {
          if (value.form) {
            dict[value.prop] = [{
              required: value.required,
              message: value.rules_message || value.label + "不能为空",
              trigger: value.trigger || "blur"
            }]
          }
        })
        console.log(2, dict)
        return dict
      },
      /** 提交按钮 */
      submitForm() {
        this.$refs["form"].validate(valid => {
          if (valid) {
            if (this.form.id !== undefined) {
              this.submitFormApi(this.form).then(response => {
                this.msgSuccess("修改成功");
                this.open = false;
                this.getTableData();
              });
            } else {
              this.submitFormApi(this.form).then(response => {
                this.msgSuccess("新增成功");
                this.open = false;
                this.getTableData();
              });
            }
          }
        })
      },
      // 取消按钮
      cancel() {
        this.open = false;
      },
      // 获取操作的权限列表
      getOperationPermis() {
        let Permis = []
        this.funcs.map(value => {
          if (['update', 'delete', 'select'].indexOf(value.type) !== 0) {
            Permis.push(value.permis)
          }
        })
        return Permis
      },
      /** 下载模板操作 */
      importTemplate() {
        this.funcs.map(value => {
          if (value.type === 'import') {
            this.importApi = value
          }
        })
        this.importApi.template_api().then(response => {
          this.download(response.data.file_url, response.data.name)
        })
      },
      // 文件上传中处理
      handleFileUploadProgress(event, file, fileList) {
        this.upload.isUploading = true
      },
      // 文件上传成功处理
      handleFileSuccess(response, file, fileList) {
        this.funcs.map(value => {
          if (value.type === 'import') {
            this.importApi = value
          }
        })
        this.upload.open = false
        this.upload.isUploading = false
        this.$refs.upload.clearFiles()
        // 是否更新已经存在的用户数据
        this.importApi.api({
          file_url: response.data.file_url,
          updateSupport: this.upload.updateSupport
        }).then(response => {
          this.$alert('导入成功！', '导入结果', {dangerouslyUseHTMLString: true})
          this.getTableData()
        })
      },
      // 提交上传文件
      submitFileForm() {
        this.$refs.upload.submit()
      }
    }
  };
</script>

<style scoped>
  .picker {
    width: 240px;
  }

  .el-pagination {
    padding: 5px;
  }

  .right_pagination {
    text-align: right;
    padding-top: 20px;
  }
</style>
