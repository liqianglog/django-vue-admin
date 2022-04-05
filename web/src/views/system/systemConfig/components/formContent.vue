<template>
  <div>
    <el-row :gutter="10">
      <el-col :span="4">变量标题</el-col>
      <el-col :span="12">变量值</el-col>
      <el-col :span="4" :offset="4">变量名</el-col>
    </el-row>
    <el-form ref="form" :model="form" label-width="100px" label-position="left" style="margin-top: 20px">
      <el-form-item :label="item.title" :prop="['array'].indexOf(item.form_item_type_label) >-1?'':item.key"
                    :key="index" :rules="item.rule"
                    v-for="(item,index) in formList"

      >
        <el-col :span="12" :offset="2">
          <!--    文本      -->
          <el-input :key="index" v-if="['text','textarea'].indexOf(item.form_item_type_label) >-1"
                    :type="item.form_item_type_label"
                    v-model="form[item.key]" :placeholder="item.placeholder" clearable></el-input>

          <el-input-number :key="index" v-else-if="item.form_item_type_label==='number'" v-model="form[item.key]"
                           :min="0"></el-input-number>
          <!--     图片     -->
          <div v-else-if="['img','imgs'].indexOf(item.form_item_type_label) >-1" :key="index">
            <el-upload
              :action="imgUploadUrl"
              :headers="uploadHeaders"
              name="url"
              :accept="'image/*'"
              :on-preview="handlePictureCardPreview"
              :on-success="(response, file, fileList)=>{handleUploadSuccess(response, file, fileList,item.key)}"
              :on-error="handleError"
              :on-exceed="handleExceed"
              :limit="item.form_item_type_label==='img'?1:5"
              :ref="'imgUpload_'+item.key"
              :data-keyname="item.key"
              :file-list="item.value?item.value:[]"
              list-type="picture-card"
            >
              <i class="el-icon-plus"></i>
              <div slot="tip" class="el-upload__tip">选取图片后,需手动上传到服务器,并且只能上传jpg/png文件</div>
            </el-upload>
            <el-dialog :visible.sync="dialogImgVisible">
              <img width="100%" :src="dialogImageUrl" alt="">
            </el-dialog>
          </div>
          <!--    关联表      -->
          <div v-else-if="['foreignkey','manytomany'].indexOf(item.form_item_type_label) >-1" :key="index">
            <table-selector
              v-model="form[item.key]"
              :el-props='{
              pagination: true,
              columns: item.setting.searchField}'
            :dict="{
              url:'/api/system/system_config/get_table_data/'+item.id+'/',
               value: item.setting.primarykey,
                label: item.setting.field,
            }"
            :pagination="true"
              :multiple="item.form_item_type_label==='manytomany'?true:false"
            ></table-selector>
          </div>
          <!--   数组       -->
          <div v-else-if="item.form_item_type_label==='array'" :key="index">
            <vxe-table
              border
              resizable
              auto-resize
              show-overflow
              keep-source
              :ref="'xTable_'+item.key"
              height="200"
              :edit-rules="validRules"
              :edit-config="{trigger: 'click', mode: 'row', showStatus: true}">
              <vxe-column field="title" title="标题" :edit-render="{autofocus: '.vxe-input--inner'}">
                <template #edit="{ row }">
                  <vxe-input v-model="row.title" type="text"></vxe-input>
                </template>
              </vxe-column>
              <vxe-column field="key" title="键名" :edit-render="{autofocus: '.vxe-input--inner'}">
                <template #edit="{ row }">
                  <vxe-input v-model="row.key" type="text"></vxe-input>
                </template>
              </vxe-column>
              <vxe-column field="value" title="键值" :edit-render="{}">
                <template #edit="{ row }">
                  <vxe-input v-model="row.value" type="text"></vxe-input>
                </template>
              </vxe-column>
              <vxe-column title="操作" width="100" show-overflow>
                <template #default="{ row,index }">
                  <el-popover
                    placement="top"
                    width="160"
                    v-model="childRemoveVisible">
                    <p>删除后无法恢复,确定删除吗？</p>
                    <div style="text-align: right; margin: 0">
                      <el-button size="mini" type="text" @click="childRemoveVisible = false">取消</el-button>
                      <el-button type="primary" size="mini" @click="onRemoveChild(row,index)">确定</el-button>
                    </div>
                    <el-button type="text" slot="reference">删除</el-button>
                  </el-popover>
                </template>
              </vxe-column>
            </vxe-table>
            <div>
              <el-button size="mini" @click="onAppend('xTable_'+item.key)">追加</el-button>
            </div>
          </div>
        </el-col>
        <el-col :span="4" :offset="6">{{ editableTabsItem.key }}.{{ item.key }}</el-col>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">确定</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import * as api from '../api'
import util from '@/libs/util'
import tableSelector from '@/components/table-selector/table-selector'

export default {
  name: 'formContent',
  inject: ['refreshView'],
  components: {
    tableSelector
  },
  props: {
    options: {
      type: Object
    },
    editableTabsItem: {
      type: Object
    }
  },
  watch: {
    options: {
      handler (nv) {
        if (nv && nv.id) {
          this.getInit()
        }
      },
      immediate: true
    }
  },
  data () {
    return {
      formList: [],
      form: {},
      childTableData: [],
      childRemoveVisible: false,
      validRules: {
        title: [
          {
            required: true,
            message: '必须填写'
          }
        ],
        key: [
          {
            required: true,
            message: '必须填写'
          }
        ],
        value: [
          {
            required: true,
            message: '必须填写'
          }
        ]
      },
      imgUploadUrl: util.baseURL() + 'api/system/img/',
      // imgUploadUrl: 'http://public.yuanxiaotian.com:8000/api/system/img/',
      uploadHeaders: {
        Authorization: 'JWT ' + util.cookies.get('token')
      },
      dialogImageUrl: '',
      dialogImgVisible: false,
      uploadImgKey: null
    }
  },
  methods: {
    // 获取数据
    getInit () {
      const that = this
      api.GetList({ parent: this.options.id }).then(res => {
        const { data } = res.data
        this.formList = data
        const form = {}
        for (const item of data) {
          const key = item.key
          form[key] = item.value
          if (item.form_item_type_label === 'array') {
            that.$nextTick(() => {
              const tableName = 'xTable_' + key
              const $table = this.$refs[tableName][0]
              $table.loadData(item.chinldern)
            })
          }
        }
        this.form = JSON.parse(JSON.stringify(form))
      })
    },
    // 提交数据
    onSubmit () {
      const that = this
      const form = JSON.parse(JSON.stringify(this.form))
      const keys = Object.keys(form)
      const values = Object.values(form)
      for (const index in this.formList) {
        const item = this.formList[index]
        // eslint-disable-next-line camelcase
        const form_item_type_label = item.form_item_type_label

        // eslint-disable-next-line camelcase
        if (form_item_type_label === 'array') {
          const parentId = item.id
          const tableName = 'xTable_' + item.key
          const $table = this.$refs[tableName][0]
          const { tableData } = $table.getTableData()
          for (const child of tableData) {
            if (!child.id && child.key && child.value) {
              child.parent = parentId
              child.id = null
              this.formList.push(child)
            }
          }
          // 必填项的判断
          for (const arr of item.rule) {
            if (arr.required && tableData.length === 0) {
              that.$message.error(item.title + '不能为空')
              return
            }
          }
          item.value = tableData
        }
        // 赋值操作
        if (keys[index] === item.key) {
          if (item.form_item_type_label !== 'array') {
            item.value = values[index]
          }
          // 必填项的验证
          if (['img', 'imgs'].indexOf(item.form_item_type_label) > -1) {
            for (const arr of item.rule) {
              if (arr.required && item.value === null) {
                that.$message.error(item.title + '不能为空')
                return
              }
            }
          }
        }
      }
      that.$refs.form.clearValidate()
      that.$refs.form.validate((valid) => {
        console.log(this.formList)
        if (valid) {
          api.saveContent(this.options.id,
            this.formList).then(res => {
            this.$message.success('保存成功')
            this.refreshView()
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    // 追加
    async onAppend (tableName) {
      const $table = this.$refs[tableName][0]
      const { tableData } = $table.getTableData()
      const tableLength = tableData.length
      if (tableLength !== 0) {
        const errMap = await $table.validate().catch(errMap => errMap)
        if (errMap) {
          this.$message.error('校验不通过！')
        }
      }
    },
    // 子表删除
    onRemoveChild (row, index) {
      if (row.id) {
        console.log(1, 'ok')
      } else {
        this.childTableData.splice(index, 1)
      }
    },
    // 图片预览
    handlePictureCardPreview (file) {
      this.dialogImageUrl = file.url
      this.dialogImgVisible = true
    },
    // 上传提交
    submitUpload (key) {
      const refName = 'imgUpload_' + key
      const ref = this.$refs[refName][0]
      ref.submit()
      this.uploadImgKey = key
    },
    // 判断是否为图片
    // 封装一个判断图片文件后缀名的方法
    isImage (fileName) {
      if (typeof fileName !== 'string') return
      const name = fileName.toLowerCase()
      return name.endsWith('.png') || name.endsWith('.jpeg') || name.endsWith('.jpg') || name.endsWith('.png') || name.endsWith('.bmp')
    },
    // 上传成功
    handleUploadSuccess (response, file, fileList, imgKey) {
      const that = this
      const {
        code,
        msg
      } = response
      if (code === 2000) {
        const { url } = response.data.data
        const { name } = file
        const type = that.isImage(name)
        if (!type) {
          this.$message.error('只允许上传图片')
        } else {
          const uploadImgKey = that.form[imgKey]
          if (!uploadImgKey) {
            that.form[imgKey] = []
          }
          // console.log(len)
          const dict = {
            name: name,
            url: url
          }
          that.form[imgKey].push(dict)
        }
      } else {
        this.$message.error('上传失败,' + JSON.stringify(msg))
      }
    },
    // 上传失败
    handleError () {
      this.$message.error('上传失败')
    },
    // 上传超出限制
    handleExceed () {
      this.$message.error('超过文件上传数量')
    }
  },
  mounted () {
    // this.getInit()
  }
}
</script>

<style scoped>

</style>
