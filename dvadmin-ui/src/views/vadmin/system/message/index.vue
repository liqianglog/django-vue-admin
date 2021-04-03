<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="公告标题" prop="title">
        <el-input
          v-model="queryParams.title"
          placeholder="请输入公告标题"
          clearable
          size="small"
          style="width: 240px"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="公告类型" prop="message_type">
        <el-select v-model="queryParams.message_type" placeholder="公告类型" clearable size="small">
          <el-option
            v-for="dict in MessagePushTypeOptions"
            :key="dict.dictValue"
            :label="dict.dictLabel"
            :value="dict.dictValue"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="公告状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="公告状态" clearable size="small">
          <el-option
            v-for="dict in MessagePushStatusOptions"
            :key="dict.dictValue"
            :label="dict.dictLabel"
            :value="dict.dictValue"
          />
        </el-select>
      </el-form-item>
      <!--      <el-form-item label="是否审核" prop="is_reviewed">-->
      <!--        <el-select v-model="queryParams.is_reviewed" placeholder="是否审核" clearable size="small">-->
      <!--          <el-option :key="true" label="是" :value="true"/>-->
      <!--          <el-option :key="false" label="否" :value="false"/>-->
      <!--        </el-select>-->
      <!--      </el-form-item>-->
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="primary"
          plain
          icon="el-icon-plus"
          size="mini"
          @click="handleAdd"
          v-hasPermi="['system:message:post']"
        >发布公告
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="el-icon-edit"
          size="mini"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['system:message:{id}:put']"
        >修改公告
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="el-icon-delete"
          size="mini"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['permission:menu:{id}:delete']"
        >删除公告
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="el-icon-download"
          size="mini"
          @click="handleExport"
          v-hasPermi="['system:message:export:get']"
        >导出
        </el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="configList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center"/>
      <el-table-column label="公告主键" align="center" prop="id"/>
      <el-table-column label="公告标题" align="center" prop="title" :show-overflow-tooltip="true"/>
      <el-table-column label="公告内容" align="center" prop="content" :show-overflow-tooltip="true"/>
      <el-table-column label="公告类型" align="center" prop="message_type" :formatter="typeFormat"/>
      <!--      <el-table-column label="是否审核通过" align="center" prop="is_reviewed" :formatter="isReviewedFormat"/>-->
      <el-table-column label="公告状态" align="center" prop="status" :formatter="statusFormat"/>
      <el-table-column label="跳转路径" align="center" prop="to_path" :show-overflow-tooltip="true"/>
      <el-table-column label="创建时间" align="center" prop="create_datetime" width="180">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.create_datetime) }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        align="center"
        class-name="small-padding fixed-width"
        v-if="hasPermi(['system:message:{id}:put','permission:menu:{id}:delete'])">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['system:message:{id}:put']"
          >修改
          </el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['permission:menu:{id}:delete']"
          >删除
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

    <!-- 添加或修改公告配置对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="780px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-row>
          <el-col :span="12">
            <el-form-item label="公告标题" prop="title">
              <el-input v-model="form.title" placeholder="请输入公告标题"/>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="跳转路径" prop="to_path">
              <el-input v-model="form.to_path" placeholder="请输入跳转路径"/>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-radio-group v-model="form.status">
                <el-radio
                  v-for="dict in MessagePushStatusOptions"
                  :key="dict.dictValue"
                  :label="dict.dictValue"
                >{{dict.dictLabel}}
                </el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="公告类型" prop="message_type">
              <el-select v-model="form.message_type" placeholder="请选择">
                <el-option
                  v-for="dict in MessagePushTypeOptions"
                  :key="dict.dictValue"
                  :label="dict.dictLabel"
                  :value="dict.dictValue"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="公告内容" prop="content">
              <editor v-model="form.content" :min-height="192"/>
            </el-form-item>
          </el-col>

          <!--        <el-form-item label="是否审核" prop="is_reviewed">-->
          <!--          <el-radio-group v-model="form.is_reviewed">-->
          <!--            <el-radio :label="true">是</el-radio>-->
          <!--            <el-radio :label="false">否</el-radio>-->
          <!--          </el-radio-group>-->
          <!--        </el-form-item>-->
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
  import {addMessage, delMessage, exportMessage, getMessage, listMessage, updateMessage} from "@/api/vadmin/system/message";
  import Editor from '@/components/Editor';

  export default {
    name: "Message",
    components: {
      Editor
    },
    data() {
      return {
        // 遮罩层
        loading: true,
        // 选中数组
        ids: [],
        // 非单个禁用
        single: true,
        // 非多个禁用
        multiple: true,
        // 显示搜索条件
        showSearch: true,
        // 总条数
        total: 0,
        // 公告表格数据
        configList: [],
        // 弹出层标题
        title: "",
        // 是否显示弹出层
        open: false,
        // 公告类型字典
        MessagePushTypeOptions: [],
        // 公告状态字典
        MessagePushStatusOptions: [],
        // 查询公告
        queryParams: {
          pageNum: 1,
          pageSize: 10,
          title: undefined,
          content: undefined,
          message_type: undefined,
          is_reviewed: undefined,
          status: undefined
        },
        // 表单公告
        form: {},
        // 表单校验
        rules: {
          title: [
            {required: true, message: "公告标题不能为空", trigger: "blur"}
          ],
          content: [
            {required: true, message: "公告内容不能为空", trigger: "blur"}
          ],
          to_path: [
            {required: false, message: "跳转路径不能为空", trigger: "blur"}
          ]
        }
      };
    },
    created() {
      this.getList();
      this.getDicts("sys_message_push_type").then(response => {
        this.MessagePushTypeOptions = response.data;
      });
      this.getDicts("sys_message_push_status").then(response => {
        this.MessagePushStatusOptions = response.data;
      });
    },
    methods: {
      /** 查询公告列表 */
      getList() {
        this.loading = true;
        listMessage(this.addDateRange(this.queryParams)).then(response => {
            this.configList = response.data.results;
            this.total = response.data.count;
            this.loading = false;
          }
        );
      },
      // 公告类型字典翻译
      typeFormat(row, column) {
        return this.selectDictLabel(this.MessagePushTypeOptions, row.message_type);
      },
      // 公告状态字典翻译
      statusFormat(row, column) {
        return this.selectDictLabel(this.MessagePushStatusOptions, row.status);
      },
      // 公告状态字典翻译
      isReviewedFormat(row, column) {
        return row.is_reviewed === true ? '是' : '否'
      },
      // 取消按钮
      cancel() {
        this.open = false;
        this.reset();
      },
      // 表单重置
      reset() {
        this.form = {
          id: undefined,
          title: undefined,
          content: undefined,
          to_path: undefined,
          is_reviewed: true,
          message_type: this.selectDictDefault(this.MessagePushStatusOptions),
          status: this.selectDictDefault(this.MessagePushStatusOptions),
        };
        this.resetForm("form");
      },
      /** 搜索按钮操作 */
      handleQuery() {
        this.queryParams.pageNum = 1;
        this.getList();
      },
      /** 重置按钮操作 */
      resetQuery() {
        this.resetForm("queryForm");
        this.handleQuery();
      },
      /** 新增按钮操作 */
      handleAdd() {
        this.reset();
        this.open = true;
        this.title = "发布公告";
      },
      // 多选框选中数据
      handleSelectionChange(selection) {
        this.ids = selection.map(item => item.id)
        this.single = selection.length != 1
        this.multiple = !selection.length
      },
      /** 修改按钮操作 */
      handleUpdate(row) {
        this.reset();
        const id = row.id || this.ids
        getMessage(id).then(response => {
          this.form = response.data;
          this.open = true;
          this.title = "修改公告";
        });
      },
      /** 提交按钮 */
      submitForm: function () {
        this.$refs["form"].validate(valid => {
          if (valid) {
            if (this.form.id != undefined) {
              updateMessage(this.form).then(response => {
                this.msgSuccess("修改成功");
                this.open = false;
                this.getList();
              });
            } else {
              addMessage(this.form).then(response => {
                this.msgSuccess("新增成功");
                this.open = false;
                this.getList();
              });
            }
          }
        });
      },
      /** 删除按钮操作 */
      handleDelete(row) {
        const configIds = row.id || this.ids;
        this.$confirm('是否确认删除公告编号为"' + configIds + '"的数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function () {
          return delMessage(configIds);
        }).then(() => {
          this.getList();
          this.msgSuccess("删除成功");
        })
      },
      /** 导出按钮操作 */
      handleExport() {
        const queryParams = this.queryParams;
        this.$confirm('是否确认导出所有数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function () {
          return exportMessage(queryParams);
        }).then(response => {
          this.download(response.data.file_url, response.data.name);
        })
      },
    }
  };
</script>
