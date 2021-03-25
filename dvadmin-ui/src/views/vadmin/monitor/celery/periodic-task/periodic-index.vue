<!--
@description: 接口信息页面
-->
<template>
  <div class="app-container">
    <common-static-table
      ref="table"
      :data="detail"
      :fields="fields"
      selection
      @selection-change="handlePeriodicSelectionChange"
    >
      <template v-slot:enabled="scope">
        <el-switch
          :value="scope.values[scope.prop]"
          active-color="#13ce66"
          disabled
          inactive-color="#ff4949"/>
      </template>
      <template v-slot:interval="scope">
        {{ getIntervalData(scope.values[`${scope.prop}_list`]) }}
      </template>
      <template v-slot:crontab="scope">
        {{ getCrontabData(scope.values[`${scope.prop}_list`]) }}
      </template>
      <template slot="button">
        <el-button
          :size="$ELEMENT.size"
          type="primary"
          title="添加任务"
          icon="el-icon-circle-plus"
          @click="handleOpenEditPeriodicForm(true)">新增
        </el-button>
      </template>
      <!--以下是自定义新增的工具栏内容-->
      <template slot="tools">
        <el-popover placement="bottom" title="温馨提示" width="400" trigger="click" style="margin-left: 10px">
          <li>待编写</li>
          <el-button
            slot="reference"
            name="refresh"
            type="info"
            size="small"
            icon="el-icon-info"
            title="温馨提示"/>
        </el-popover>
      </template>
      <!--以下是自定义新增的列的配置内容-->
      <template slot="column">
        <el-table-column fixed="right" label="操作" align="center" width="150">
          <template slot-scope="scope">
            <el-button
              :size="$ELEMENT.size"
              type="primary"
              title="立即执行"
              icon="el-icon-caret-right"
              circle
              @click="test(scope.row)"/>
            <el-button
              :size="$ELEMENT.size"
              type="primary"
              title="编辑"
              icon="el-icon-edit"
              circle
              @click="handleOpenEditPeriodicForm(false, scope.row)"/>
            <el-button
              :size="$ELEMENT.size"
              type="danger"
              title="移除"
              icon="el-icon-delete"
              circle
              @click="handleRemovePeriodicTable(scope.$index, scope.row)"
            />
          </template>
        </el-table-column>
      </template>
    </common-static-table>
    <el-dialog :visible.sync="dialogFormVisible" title="请确认" >
      <span>
        正在同步：{{ row.task }}
      </span>
      <br>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleOperate">确 定</el-button>
      </div>
    </el-dialog>
    <edit-form-periodic-task
      v-model="editPeriodicFormVisible"
      :entity="editPeriodic"
      :create="editPeriodicCreate"
      :periodic-data="periodicData"
      :width="'40%'"
      @success="handleSuccessEditPeriodic"/>
  </div>
</template>

<script>
  import * as SyncDataApi from "@/api/vadmin/monitor/celery";
  import EditFormPeriodicTask from './edit-form-periodic-task';

  export default {
    components: { EditFormPeriodicTask },
    props: {
    },
    data() {
      return {
        fields: [
          // prop,后端列名称, 必填; label,前端表头名称, 必填; 其他可有可无
          { prop: 'name', label: '名称', show: true, unique: true },
          { prop: 'task', label: 'celery任务', show: true, width: 400 },
          { prop: 'interval', label: '频率', show: true, search: true },
          { prop: 'crontab', label: '任务编排', show: true, search: true, sortable: true },
          { prop: 'args', label: '参数', show: false, search: true, sortable: true, width: 80 },
          { prop: 'kwargs', label: '位置参数', show: false, search: true, sortable: true },
          { prop: 'queue', label: '队列', show: false, search: true, sortable: true },
          { prop: 'exchange', label: '状态', show: false, search: true },
          { prop: 'routing_key', label: '路由密钥', show: false, search: true },
          { prop: 'expires', label: '过期时间', show: false, search: true, type: 'datetime' },
          { prop: 'enabled', label: '是否开启', show: true, search: true }
        ],
        periodicData: [],
        multipleSelection: [],
        PeriodicTagList: [],
        editPeriodic: {},
        editPeriodicFormVisible: false,
        editPeriodicCreate: false,
        modelFormVisible: false,
        modelSwaggerVisible: false,
        batchEditFormVisible: false,
        detail: [],
        dialogFormVisible: false,
        form: { name: '' },
        formLabelWidth: '120px',
        row: '',
        reqloading: false,
        task_id:''
      };
    },
    computed: {
    },
    watch: {
    },
    created() {
      this.initData();
    },
    methods: {
      initData() {
        SyncDataApi.listPeriodicTask({ page_size: 1000 }).then((response) => {
          this.detail = response.data.results || [];
        });
      },
      handleRefresh(infos) {
        this.$refs.table.clearSelection();
        this.$emit('update');
      },
      handlePeriodicSelectionChange(infos) {
        this.multipleSelection = infos;
      },
      handleOpenEditPeriodicForm(create = false, info) {
        if (create) {
          this.editPeriodic = { periodic: this.detail.id };
        } else {
          this.editPeriodic = { ...info };
        }
        this.editPeriodicCreate = create;
        this.editPeriodicFormVisible = true;
      },
      handleRemovePeriodicTable(index, info) {
        this.$confirm('确认删除？', '确认信息', {
          distinguishCancelAndClose: true,
          confirmButtonText: '删除',
          cancelButtonText: '取消'
        }).then(() => {
          SyncDataApi.deletePeriodicTask(info.id).then(response => {
            const name = info.name ? info.name + ':' : '';
            this.msgSuccess(name + '删除成功');
            this.initData();
          });
        });
      },
      handleSuccessEditPeriodic() {
        this.initData();
        this.$emit('update');
      },
      handleOpenModelForm() {
        this.modelFormVisible = true;
      },
      handleOpenSwagger(model = false) {
        this.modelSwaggerVisible = true;
      },
      handleBatchEdit() {
        this.batchEditFormVisible = true;
      },
      test(row) {
        this.dialogFormVisible = true;
        this.row = row;
        this.DetailMsg = ''
      },
      handleOperate() {
        this.dialogFormVisible = false
        this.reqloading = true;
        SyncDataApi.operatesyncdata({ celery_name: this.row.task }).then(response => {
         this.task_id = response.data.task_id
          this.msgSuccess("执行成功！");
        })
      },
      closeView(){
        this.reqloading = false
      }
    }
  };
</script>

<style scoped>
  .el-table th {
    display: table-cell !important;
  }
</style>
