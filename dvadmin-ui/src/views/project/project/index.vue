<template>
  <div>
    <!--    <el-form ref="form" :model="form" label-width="80px">-->
    <!--      <el-form-item label="上级部门" prop="parentId">-->
    <!--      </el-form-item>-->
    <!--    </el-form>-->
    <!--    <dept-tree :value.sync="form.dept"></dept-tree>-->
    <!--    <users-tree :value.sync="form.dept" :multiple="true"></users-tree>-->
    <br>
    <model-display :api="api" :fields="fields">
      <template slot="button">
        <br>
        <br>
        <el-row :gutter="10" class="mb8">
          <el-col :span="1.5">
            <el-button
              type="primary"
              plain
              icon="el-icon-plus"
              size="mini"
              v-hasPermi="['permission:user:post']"
            >新增
            </el-button>
          </el-col>
          <el-col :span="1.5">
            <el-button
              type="success"
              plain
              icon="el-icon-edit"
              size="mini"
              :disabled="single"
              v-hasPermi="['permission:user:{id}:put']"
            >修改
            </el-button>
          </el-col>
          <el-col :span="1.5">
            <el-button
              type="danger"
              plain
              icon="el-icon-delete"
              size="mini"
              :disabled="multiple"
              v-hasPermi="['permission:user:{id}:delete']"
            >删除
            </el-button>
          </el-col>
          <el-col :span="1.5">
            <el-button
              type="info"
              plain
              icon="el-icon-upload2"
              size="mini"
              v-hasPermi="['permission:user:import:post']"
            >导入
            </el-button>
          </el-col>
          <el-col :span="1.5">
            <el-button
              type="warning"
              plain
              icon="el-icon-download"
              size="mini"
              v-hasPermi="['permission:user:export:get']"
            >导出
            </el-button>
          </el-col>
<!--          <right-toolbar :showSearch.sync="showSearch" @queryTable="getList" :columns="columns"></right-toolbar>-->
        </el-row>
      </template>
    </model-display>
  </div>
</template>

<script>
  import * as Project from '../../../api/project/project';

  export default {
    name: "project",
    data() {
      return {
        value: '',
        api: Project.listProject,
        form: {"dept": [2]},
        fields: [
          // prop,后端列名称, 必填; label,前端表头名称, 必填; 其他可有可无
          {prop: 'id', label: 'ID', show: false, unique: true},
          {prop: 'name', label: '项目名称', show: true, search: true},
          {prop: 'code', label: '项目编码', show: true, search: true},
          {prop: 'person', label: '项目负责人', show: true, search: true, sortable: true},
          {prop: 'dept', label: '部门', search: true},
          {prop: 'description', label: '描述', search: true}
        ],
        multipleSelection: [],
      }
    },
    created() {
    },
    mounted() {
    },
    methods: {
      handleOpenAddForm(model = false) {
        if (model) {
          this.modelFormVisible = true;
        } else {
          this.editFormCreate = true;
          this.editFormVisible = true;
        }
      },
      handleOpenSwagger(model = false) {
        this.modelSwaggerVisible = true;
      },
      handleBatchEdit() {
        this.batchEditFormVisible = true;
      },
      handleBatchDelete() {
        const count = this.multipleSelection.length;
        this.$confirm(`即将删除选择的${count}条数据？`, '确认信息', {
          type: 'warning',
          distinguishCancelAndClose: true,
          confirmButtonText: '删除',
          cancelButtonText: '取消'
        }).then(() => {
          const instanceIdList = this.multipleSelection.map(ele => ele.instanceId);
          PermissionInterfaceApi.batchDeletePermissionInterface(instanceIdList).then(response => {
            MessageUtils.showSuccessMessage('批量删除成功');
            this.handleRefresh();
          });
        }).catch(() => {
        });
      },
    }

  }
</script>

<style scoped>

</style>
