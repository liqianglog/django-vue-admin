<!--
@author: xuchi
@description: 接口信息页面
-->
<template>
  <div class="app-container">
    <el-card class="box-card" shadow="never">
      <div slot="header" class="clearfix">
        <span>任务定时</span>
        <el-button style="float: right; padding: 3px 0" type="text" @click="handleOpenEditCrontabForm(true)">
          新增定时
        </el-button>
      </div>
      <div style="height: 200px;">
        <el-scrollbar>
          <div v-for="(val,index) in detail" :key="index">
            <div class="text" style="display:inline-block;height: 10px;">
              <span>{{ getCrontabData(val) }}</span>
            </div>
            <div style="float: right;padding-right: 10px;display:inline-block">
              <el-button
                type="primary"
                icon="el-icon-edit"
                size="mini"
                circle
                @click="handleOpenEditCrontabForm(false, val)"/>
              <el-button
                type="danger"
                icon="el-icon-delete"
                size="mini"
                circle
                @click="handleRemoveCrontabTable(val)"/>
            </div>
            <el-divider/>
          </div>
          <div v-if="detail.length===0" style="text-align: center">
            暂无信息
          </div>
        </el-scrollbar>
      </div>
    </el-card>
    <edit-form-crontab-task
      v-model="editCrontabFormVisible"
      :entity="editCrontab"
      :create="editCrontabCreate"
      :periodic-data="periodicData"
      :width="'30%'"
      @success="handleSuccessEditCrontab"/>
  </div>
</template>

<script>
  import * as SyncDataApi from "@/api/vadmin/monitor/celery";
  import EditFormCrontabTask from './edit-form-crontab-task';

  export default {
    components: { EditFormCrontabTask },
    props: {
    },
    data() {
      return {
        periodicData: [],
        multipleSelection: [],
        CrontabTagList: [],
        editCrontab: {},
        editCrontabFormVisible: false,
        editCrontabCreate: false,
        modelFormVisible: false,
        modelSwaggerVisible: false,
        batchEditFormVisible: false,
        detail: []
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
        SyncDataApi.listCrontabSchedule({ page_size: 1000 }).then((response) => {
          this.detail = response.data.results || [];
          this.$store.state.Crontab = this.detail;
        });
      },
      handleRefresh(infos) {
        this.$refs.table.clearSelection();
        this.$emit('update');
      },
      handleOpenEditCrontabForm(create = false, info) {
        if (create) {
          this.editCrontab = { periodic: this.detail.id };
        } else {
          this.editCrontab = { ...info };
        }
        this.editCrontabCreate = create;
        this.editCrontabFormVisible = true;
      },
      handleRemoveCrontabTable(info) {
        this.$confirm('确认删除？', '确认信息', {
          distinguishCancelAndClose: true,
          confirmButtonText: '删除',
          cancelButtonText: '取消'
        }).then(() => {
          SyncDataApi.deleteCrontabSchedule(info.id).then(response => {
            const name = info.name ? info.name + ':' : '';
            this.msgSuccess(name + '删除成功!');
            this.initData();
          });
        });
      },
      handleSuccessEditCrontab() {
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
      }
    }
  };
</script>

<style scoped>
  .el-table th {
    display: table-cell !important;
  }
  .el-scrollbar {
      height: 100%;
  }

  .el-scrollbar__wrap {
      overflow: scroll;
      width: 100%;
      height: 100%;
  }

  .el-scrollbar__view {
      height: 100%;
  }

  .el-divider--horizontal {
      margin: 14px 0;
  }

  .text {
      padding-left: 20px;
      font-size: 14px;
  }
  .el-button--mini.is-circle {
      padding: 5px;

  }
</style>
