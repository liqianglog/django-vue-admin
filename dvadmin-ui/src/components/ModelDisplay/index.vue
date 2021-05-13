<!--
@author: ruoxing
@description: 封装组件
-->
<template>
  <div style="padding-left: 10px;">
    <el-row v-if="topLayout" style="margin-bottom: 20px">
      <el-col v-if="topLayoutLeft" :span="18">
        <div class="grid-content bg-purple">
          <el-input
            v-model="searchForm.search"
            :disabled="tableLoading"
            :size="$ELEMENT.size"
            :placeholder="searchPlaceholder"
            clearable
            style="width: 200px;"
            @keyup.enter.native="handleSearchFormSubmit"/>
          <el-button
            :size="$ELEMENT.size"
            name="search"
            type="primary"
            icon="el-icon-search"
            title="模糊查询"
            @click="handleSearchFormSubmit"/>
          <el-button
            v-show="searchFormShow"
            :size="$ELEMENT.size"
            name="search"
            type="primary"
            title="高级搜索"
            @click="handleAdvancedSearchFormShow">高级搜索
          </el-button>
          <slot name="button"/>
        </div>
      </el-col>
      <el-col v-if="topLayoutRight" :span="6">
        <div class="grid-content bg-purple-light" style="text-align: right">
          <slot name="tools"/>
          <el-button
            :size="$ELEMENT.size"
            name="refresh"
            type="info"
            title="导出数据"
            @click="handleExportTableData">
            <svg-icon icon-class="icon-excel" style="font-size: 1em"/>
          </el-button>
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

    <el-collapse v-show="showAdvancedSearchForm" value="as">
      <el-collapse-item title="高级搜索功能" name="as">
        <advanced-search-form
          ref="advancedForm"
          v-model="advancedSearchForm"
          :fields="advancedSearchFields"
          :size="$ELEMENT.size"
          @submit="handleAdvancedSearchFormSubmit"
          @reset="handleAdvancedSearchFormReset"/>
      </el-collapse-item>
    </el-collapse>

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
    <!--<avue-crud :data="tableData" :option="tableOption" :page="tablePagination" @row-save="rowSave"/>-->
<!--    <table-export-dialog-->
<!--      v-model="excelDialogVisible"-->
<!--      :dialog-drag="dialogDrag"-->
<!--      :fields="exportFields"-->
<!--      :data="tableData"-->
<!--      :selection="selection"-->
<!--      :selected-data="multipleSelection"-->
<!--      append-to-body-->
<!--      width="40%"-->
<!--      dialog-title="数据导出"/>-->
  </div>
</template>
<script>
  import moment from 'moment';
  import * as Utils from '@/utils';
  import request from '@/utils/request';

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
      searchPlaceholder: {
        type: String,
        default: '模糊搜索'
      },
      emptyText: {
        type: String,
        default: '暂无数据'
      },
      dialogDrag: {type: Boolean, default: false},
      axios: {
        type: Object,
        default: () => {
        }
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
      api: {
        // 用于替换method + url属性
        type: Function,
        default: null
      },
      url: {
        // 后端接口uri(必选), 已废用。请使用api代替
        type: String,
        default: ''
      },
      method: {
        // 后端接口方法(默认, GET), 已废用。请使用api代替
        type: String,
        default: 'get'
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
      selection: {
        // 开始开启多选(默认不开启, false)
        type: Boolean,
        default: false
      },
      params: {
        // 基本请求参数,最终请求参数=基本参数+基本高级搜索参数+组件封装的基本参数+租金组件封装的高级搜索参数
        type: Object,
        default: () => {
          return {};
        }
      },
      baseParams: {
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
        tableEditable: true,
        showFields: [], // 显示的字段
        buttonTagList: [], // 所有按钮标签
        searchForm: {
          search: '',
          ordering: ''
        },
        excelDialogVisible: false,
        tableLoading: false,
        showAdvancedSearchForm: false,
        advancedSearchForm: {},
        advancedSearchFields: [],
        tableData: [],
        rowKey: '',
        multipleSelection: [],
        pagination: {
          page: 1,
          page_size: 10,
          total: 0
        },
        excelHeader: [],
        excelData: [],
        getRowKeys: row => {
          if (this.rowKey) {
            return row[this.rowKey];
          }
          return row.id || row.uuid;
        },
        exportFields: [],
        fields1: [],
        tableOption: {},
        tablePagination: {},
        asParams: {}
      };
    },
    computed: {
      topLayoutLeft() {
        return this.topLayout.indexOf('left') >= 0;
      },
      topLayoutRight() {
        return this.topLayout.indexOf('right') >= 0;
      },
      searchFormShow() {
        return this.advancedSearchFields.length > 0;
      }
    },
    watch: {
      params: {
        deep: true,
        handler: function (newValue, oldValue) {
          this.getTableData();
        }
      },
      baseParams: {
        deep: true,
        handler: function (newValue, oldValue) {
          this.getTableData();
        }
      }
    },
    mounted() {
    },
    created() {
      // this.getTableOption();
      this.initComponentData();
      this.initAdvancedSearchFields();
      this.getTableData();
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
      initAdvancedSearchFields() {
        this.advancedSearchFields = this.fields
          .filter(field => field.search)
          .map(field => {
            return {...field};
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
      sortMethod(a, b) {
        return -1;
      },
      getTableData() {
        this.listInterfaceData(this.getRequestParams());
        return this.tableData;
      },
      reset(refresh = false) {
        this.tableData = [];
        this.pagination = {page: 1, page_size: this.pageSizes[0], total: this.tableData.length};
        if (refresh) {
          this.getTableData();
        }
      },
      rowSave(row, done, loading) {
        console.dir(row);
        done();
      },
      async getTableOption() {
        const url = this.url;
        const method = this.method;
        await request({
          url,
          method,
          params: {query_type: 'tableOption'}
        }).then(response => {
          this.tableOption = response.data.option;
          this.tablePagination = response.data.page;
        }).catch(error => {
          console.error(error);
        });
        this.initComponentData();
        this.initAdvancedSearchFields();
        this.getTableData();
      },
      getMultipleSelection() {
        return this.multipleSelection || [];
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
        const asForm = {};
        const tmpAsParams = {...this.baseParams, ...JSON.parse(JSON.stringify(this.asParams))};
        for (const prop of Object.keys(tmpAsParams)) {
          if (tmpAsParams[prop]) {
            asForm[prop] = tmpAsParams[prop];
          }
        }
        const tmpParams = {...this.params, ...this.getFormattedPaginationParams()};
        const params = {};
        for (const prop of Object.keys(tmpParams)) {
          if (tmpParams[prop]) {
            params[prop] = tmpParams[prop];
          }
        }
        if (Object.keys(asForm).length) {
          params['as'] = JSON.stringify(asForm);
        }
        // 组装普遍模糊搜索的参数
        if (this.searchForm.search) {
          params['search'] = this.searchForm.search;
        }
        // 组装普遍模糊搜索的参数
        if (this.searchForm.ordering) {
          params['ordering'] = this.searchForm.ordering;
        }
        // console.dir(params);
        return params;
      },
      // 封装后端接口, 后端接口返回数据必须规范一致
      listInterfaceData(params) {
        this.tableLoading = true;
        this.api(params).then(response => {
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
      clearMultipleSelection() {
        this.clearSelection();
      },
      clearSelection() {
        this.$refs.tableData.clearSelection();
      },
      handleSelectField(e, field) {
        field.show = e;
      },
      // 处理点击高级搜索按钮事件
      handleAdvancedSearchFormSubmit(params) {
        this.pagination.page = 1;
        this.asParams = params;
        this.listInterfaceData(this.getRequestParams());
      },
      handleAdvancedSearchFormReset() {
        this.advancedSearchForm = {};
      },
      // 处理提交表单, 点击搜索按钮事件
      handleSearchFormSubmit() {
        this.pagination.page = 1;
        this.getTableData();
      },
      // 处理显示/隐藏高级搜索表单按钮点击事件
      handleAdvancedSearchFormShow() {
        this.showAdvancedSearchForm = !this.showAdvancedSearchForm;
      },
      handleEditFormSubmit(form, done) {
        done();
        this.handleCloseEditDialog();
      },
      // 导出表格的数据, 当前数据、当前列
      handleExportTableData() {
        this.excelDialogVisible = true;
        this.exportFields = this.fields.map(field => {
          return {prop: field.prop, label: field.label, show: field.show};
        });
        this.excelHeader = this.showFields.map(field => field['prop']);
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
      handleOpenEditDialog(row) {
        this.editForm = {...row};
        this.editDialogVisible = true;
      },
      handleCloseEditDialog() {
        this.editDialogVisible = false;
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
