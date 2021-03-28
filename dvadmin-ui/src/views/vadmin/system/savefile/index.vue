<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="文件名称" prop="name">
        <el-input
          v-model="queryParams.name"
          placeholder="请输入文件名称"
          clearable
          size="small"
          style="width: 240px"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="文件类型" prop="type">
        <el-input
          v-model="queryParams.type"
          placeholder="请输入文件类型"
          clearable
          size="small"
          style="width: 240px"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
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
          icon="el-icon-upload"
          size="mini"
          @click="handleAdd"
          v-hasPermi="['system:savefile:post']"
        >文件上传
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
          v-hasPermi="['system:savefile:{id}:delete']"
        >批量删除
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="el-icon-download"
          size="mini"
          @click="handleClear"
          v-hasPermi="['system:clearsavefile:post']"
        >清理废弃文件
        </el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="fileList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center"/>
      <el-table-column label="文件编号" width="90" align="center" prop="id"/>
      <el-table-column label="文件名称" width="200" align="center" prop="name" :show-overflow-tooltip="true"/>
      <el-table-column label="文件类型" width="150" align="center" prop="type"/>
      <el-table-column label="文件大小" width="90" align="center" prop="size"/>
      <el-table-column label="存储位置" align="center" prop="address"/>
      <el-table-column label="文件来源" align="center" prop="source"/>
      <el-table-column label="文件本地地址" align="center" prop="file" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-document-copy"
            @click="CopyFileUrl(scope.row.file)"
            v-if="scope.row.file"
          ></el-button>
          &nbsp;
          <span>{{ scope.row.file }}</span>
        </template>
      </el-table-column>
      <el-table-column label="OSS地址" align="center" prop="oss_url" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-document-copy"
            @click="CopyFileUrl(scope.row.oss_url)"
            v-if="scope.row.oss_url"
          ></el-button>
          &nbsp;
          <span>{{ scope.row.oss_url }}</span>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" align="center" prop="create_datetime" width="160">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.create_datetime) }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        align="center"
        class-name="small-padding fixed-width"
        width="130"
        v-if="hasPermi(['system:clearsavefile:download:post'])"
      >
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-download"
            @click="handleDownload(scope.row)"
            v-hasPermi="['system:clearsavefile:download:post']"
          >下载
          </el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['system:savefile:{id}:delete']"
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
    <!-- 对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="400px" append-to-body @close="submitForm">
      <FileUpload ref="saveFile" :file-type="['ALL']" @input="submitForm"></FileUpload>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">完 成</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
  import {clearSaveFile, delSaveFile, listSaveFile} from "@/api/vadmin/system/savefile";
  import FileUpload from "@/components/FileUpload/index";

  export default {
    name: "Savefile",
    components: {FileUpload},
    data() {
      return {
        // 遮罩层
        loading: true,
        // 显示搜索条件
        showSearch: true,
        // 非单个禁用
        single: true,
        // 非多个禁用
        multiple: true,
        // 弹出层标题
        title: "",
        // 是否显示弹出层
        open: false,
        // 查询参数
        queryParams: {
          pageNum: 1,
          pageSize: 10,
          name: undefined,
          type: undefined,
        },
        // 总条数
        total: 0,
        // 数据列表
        fileList: [],
      }
    },
    created() {
      this.getList();
    },
    mounted() {
    },
    methods: {
      /** 查询列表 */
      getList() {
        this.loading = true;
        listSaveFile(this.queryParams).then(response => {
          this.fileList = response.data.results;
          this.total = response.data.count;
          this.loading = false;
        });
      },
      /** 搜索按钮操作 */
      handleQuery() {
        this.getList();
      },
      /** 重置按钮操作 */
      resetQuery() {
        this.resetForm("queryForm");
        this.handleQuery();
      },
      /** 上传按钮操作 */
      handleAdd(row) {
        this.open = true;
        this.title = "上传文件";
      },
      /** 文件下载 **/
      handleDownload(row) {
        this.download(row.file_url, row.name)
      },
      /** 删除按钮操作 */
      handleDelete(row) {
        const userIds = row.id || this.ids;
        this.$confirm('是否确认删除文件编号为"' + userIds + '"的数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function () {
          return delSaveFile(userIds);
        }).then(() => {
          this.getList();
          this.msgSuccess("删除成功");
        })
      },
      // 多选框选中数据
      handleSelectionChange(selection) {
        this.ids = selection.map(item => item.id)
        this.single = selection.length !== 1
        this.multiple = !selection.length
      },
      /** 清理废弃文件 */
      handleClear() {
        this.$confirm('此项操作会把所有数据库中不存在的文件删除，包括OSS中的文件，是否确认要清理废弃文件?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function () {
          return clearSaveFile();
        }).then((values) => {
          this.getList();
          this.msgSuccess(values.msg);
        })
      },
      /** 完成按钮 */
      submitForm: function () {
        this.getList();
        this.open = false;
        this.$refs.saveFile.fileList = []
      },
      CopyFileUrl(values){
        const input = document.createElement('input');
        document.body.appendChild(input);
        input.setAttribute('value', values);
        input.select();
        if (document.execCommand('copy')) {
          document.execCommand('copy');
          this.msgSuccess("复制成功");
        }
        document.body.removeChild(input);
      }
    }

  }
</script>

<style scoped>

</style>
