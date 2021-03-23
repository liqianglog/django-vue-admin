<!--
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
            :placeholder="filterPlaceholder"
            clearable
            style="width: 200px;"
            @keyup.enter.native="handleSearchFormSubmit"/>
          <el-button
            :size="$ELEMENT.size"
            type="primary"
            title="过滤"
            @click="handleSearchFormSubmit">
            <common-icon value="svg:icon-filter"/>
          </el-button>
          <el-button
            v-show="isFilter"
            :size="$ELEMENT.size"
            type="info"
            title="取消过滤"
            style="margin-left: 0;"
            @click="handleCancelFilter">
            <common-icon value="svg:icon-unfilter"/>
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
                <el-checkbox
                  v-for="(field, index) in fields"
                  :key="index"
                  :label="field"
                  :checked="field.show"
                  style="width: 100%"
                  @change="handleSelectField($event, field)">{{ field.label }}</el-checkbox>
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
      ref="table"
      :data="filterData"
      :span-method="spanMethod"
      :max-height="maxHeight"
      :row-key="getRowKeys"
      :stripe="stripe"
      :fit="fit"
      :border="border"
      :empty-text="emptyText"
      :highlight-current-row="highlightCurrentRow"
      :show-overflow-tooltip="showOverflowTooltip"
      @cell-click="handleCellClick"
      @cell-dblclick="handleCellDbClick"
      @header-click="handleHeaderClick"
      @row-click="handleRowClick"
      @row-dblclick="handleRowDblClick"
      @selection-change="handleSelectionChange">
      <el-table-column
        v-if="selection"
        :reserve-selection="true"
        type="selection"
        width="50"/>
      <template v-for="field in fields">
        <el-table-column
          v-if="field.show"
          :key="field.prop"
          :prop="field.prop"
          :label="field.label"
          :sortable="field.sortable"
          :width="field.width || ''"
          show-overflow-tooltip>
          <template slot-scope="scope">
            <slot :name="field.prop" :values="scope.row" :prop="field.prop" :field="field">
              <span v-html="formatColumnData(scope.row, field)"/>
            </slot>
          </template>
        </el-table-column>
      </template>
      <slot name="column"/>
    </el-table>
    <el-row>
      <el-col :span="6" style="margin-top: 20px">
        <span>已选择:<span style="color: #ff00ff;font-weight: bold;">{{ multipleSelection.length }}</span>条</span>
        <el-button
          v-show="multipleSelection.length"
          type="info"
          size="mini"
          title="清空多选"
          @click="clearMultipleSelection">清空</el-button>
      </el-col>
      <el-col :span="18" style="margin-top: 20px; text-align: right">
        <span>总计:<span style="color: #ff00ff;font-weight: bold;">{{ filterData.length }}</span>条</span>
      </el-col>
    </el-row>
  </div>
</template>
<script>
  import moment from 'moment';
  import * as Utils from '@/utils';
  export default {
    name: 'CommonStaticTable',
    props: {
      value: {
        type: Array,
        default: () => []
      },
      spanMethod: {
        type: Function,
        default: null
      },
      data: {
        type: Array,
        default: () => []
      },
      initSelected: {
        type: Array,
        default: () => []
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
      topLayout: {
        type: Array,
        default: () => {
          return ['left', 'right'];
        }
      },
      bottomLayout: {
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
      // api 对象
      api: {
        type: Function,
        default: null
      },
      params: {
        type: Object,
        default: () => {
          return {};
        }
      }
    },
    data() {
      return {
        tableEditable: true,
        showFields: [], // 显示的字段
        filterFields: [], // 过滤的字段
        filterPlaceholder: '过滤', // 过滤提示文字
        buttonTagList: [], // 所有按钮标签
        excelDialogVisible: false,
        tableLoading: false,
        advancedSearchForm: {},
        advancedSearchFields: [],
        rowKey: null,
        multipleSelection: [],
        excelHeader: [],
        excelData: [],
        searchForm: {
          search: ''
        },
        getRowKeys: row => {
          if (this.rowKey) {
            return row[this.rowKey];
          }
          return row.id || row.uuid;
        },
        exportFields: [],
        tableData: [],
        filterData: [],
        isFilter: false
      };
    },
    computed: {
      topLayoutLeft() {
        return this.topLayout.indexOf('left') >= 0;
      },
      topLayoutRight() {
        return this.topLayout.indexOf('right') >= 0;
      }
    },
    watch: {
      data: {
        handler: function(newData, oldData) {
          this.handleChangeTableData(newData);
        },
        immediate: true
      }
    },
    mounted() {
    },
    created() {
      this.initComponentData();
      this.initData();
      this.initSelect();
    },
    methods: {
      initData() {
        if (Utils.isFunction(this.api)) {
          this.listInterfaceData();
        }
      },
      initSelect() {
        for (const row of this.initSelected) {
          this.$refs['table'].toggleRowSelection(row, true);
        }
      },
      initComponentData() {
        this.fields.forEach(field => {
          field.show = (!!field.show);
          field.type = (field.type || 'string').toLocaleLowerCase();
          field.label = field.label || field.prop;
          field.search = (!!field.search);
          field.sortable = (!!field.sortable);
          field.unique = (!!field.unique);
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
        this.filterFields = this.fields.filter(field => field.search).map(field => field.prop);
        if (this.filterFields.length) {
          const text = this.fields.filter(field => field.search).map(field => field.label).join('、');
          this.filterPlaceholder = `${text} 过滤`;
        }
      },
      listInterfaceData() {
        this.tableLoading = true;
        this.api(this.params).then(response => {
          this.tableLoading = false;
          this.handleChangeTableData(response.data);
        }).catch(() => {
          this.tableLoading = false;
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
      getMultipleSelection() {
        return this.multipleSelection || [];
      },
      clearMultipleSelection() {
        this.$refs.table.clearSelection();
      },
      clearSelection() {
        this.$refs.table.clearSelection();
      },
      clearFilter() {
        // 重置过滤
        this.searchForm.search = '';
        this.filterData = Array.from(this.tableData);
      },
      handleSelectField(e, field) {
        field.show = e;
      },
      handleChangeTableData(data) {
        this.tableData = Array.from(data);
        this.filterData = Array.from(this.filterHandler(this.tableData));
      },
      // 导出表格的数据, 当前数据、当前列
      handleExportTableData() {
        this.excelDialogVisible = true;
        this.exportFields = this.fields.map(field => {
          return { prop: field.prop, label: field.label, show: field.show };
        });
        this.excelHeader = this.showFields.map(field => field['prop']);
      },
      // 处理修改多选的值
      handleSelectionChange(val) {
        this.$emit('selection-change', val);
        this.multipleSelection = val;
      },
      handleSortChange(val) {
        this.sort.prop = val.prop;
        this.sort.order = val.order;
        this.getTableData();
      },
      filterHandler(data) {
        if (!data) {
          data = this.tableData || [];
        }
        const search = this.searchForm.search.trim();
        if (!search.length || !this.filterFields.length) {
          this.isFilter = false;
          return data;
        }
        const filterData = data.filter(row => {
          for (const field of this.filterFields) {
            if (row[field] && row[field].indexOf(search) >= 0) {
              return true;
            }
          }
          return false;
        });
        this.isFilter = true;
        return filterData;
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
      toggleRowSelection(row, selected = true) {
        this.$refs.table.toggleRowSelection(row, selected);
      },
      toggleFilter() {
        // 触发过滤
        this.filterData = Array.from(this.filterHandler());
      },
      handleSearchFormSubmit() {
        this.toggleFilter();
      },
      handleCancelFilter() {
        this.isFilter = false;
        this.clearFilter();
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
