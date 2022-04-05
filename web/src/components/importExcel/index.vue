<template>
  <div style="display: inline-block">
    <el-button size="small" type="success" icon="el-icon-upload" @click="handleImport">
      <slot>导入</slot>
    </el-button>
  <el-dialog :title="upload.title" :visible.sync="upload.open" width="400px" append-to-body>
    <el-upload
      ref="upload"
      :limit="1"
      accept=".xlsx, .xls"
      :headers="upload.headers"
      :action="upload.url"
      :disabled="upload.isUploading"
      :on-progress="handleFileUploadProgress"
      :on-success="handleFileSuccess"
      :auto-upload="false"
      drag
    >
      <i class="el-icon-upload" />
      <div class="el-upload__text">
        将文件拖到此处，或
        <em>点击上传</em>
      </div>
      <div slot="tip" class="el-upload__tip">
        <el-checkbox size="medium" label="是否更新已经存在的数据" border v-model="upload.updateSupport" />

      </div>
      <div slot="tip" class="el-upload__tip" style="color:red">提示：仅允许导入“xls”或“xlsx”格式文件！</div>
    </el-upload>
    <div><el-link type="primary" style="font-size:14px;margin-top: 20px" @click="importTemplate">下载模板</el-link></div>
    <div slot="footer" class="dialog-footer">
      <el-button type="primary" @click="submitFileForm">确 定</el-button>
      <el-button @click="upload.open = false">取 消</el-button>
    </div>
  </el-dialog>
  </div>
</template>

<script>
import util from '@/libs/util'
import { request, downloadFile } from '@/api/service'

export default {
  name: 'importExcel',
  inject: ['refreshView'],
  props: {
    upload: {
      type: Object,
      default () {
        return {
          // 是否显示弹出层
          open: false,
          // 弹出层标题
          title: '',
          // 是否禁用上传
          isUploading: false,
          // 是否更新已经存在的用户数据
          updateSupport: 0,
          // 设置上传的请求头部
          headers: { Authorization: 'JWT ' + util.cookies.get('token') },
          // 上传的地址
          url: process.env.VUE_APP_API + '/api/system/file/'
        }
      }
    },
    importApi: { // 导入接口地址
      type: String,
      default () {
        return undefined
      }
    }
  },
  methods: {
    /** 导入按钮操作 */
    handleImport () {
      this.upload.open = true
    },
    /** 下载模板操作 */
    importTemplate () {
      downloadFile({
        url: process.env.VUE_APP_API + this.importApi,
        params: {},
        method: 'get'
      })
    },
    // 文件上传中处理
    handleFileUploadProgress (event, file, fileList) {
      this.upload.isUploading = true
    },
    // 文件上传成功处理
    handleFileSuccess (response, file, fileList) {
      const that = this
      // that.upload.open = false
      that.upload.isUploading = false
      that.$refs.upload.clearFiles()
      // 是否更新已经存在的用户数据
      return request({
        url: that.importApi,
        method: 'post',
        data: {
          url: response.data.url,
          updateSupport: that.upload.updateSupport
        }
      }).then(response => {
        // this.$alert("导入成功！", "导入结果", { dangerouslyUseHTMLString: true });
        that.$alert('导入成功', '导入完成', {
          confirmButtonText: '确定',
          callback: action => {
            that.refreshView()
          }
        })
      })
    },
    // 提交上传文件
    submitFileForm () {
      this.$refs.upload.submit()
    }
  }
}
</script>

<style scoped>

</style>
