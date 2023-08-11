<template>
  <div>
    <el-row>
      <el-col :span="elProps.index.span" v-if="elProps.index">
        <div style="text-align: center">{{ elProps.index.name }}</div>
      </el-col>
      <el-col :span="elProps.fields[key].span" v-for="(_, key) in elProps.fields" :key="key">
        <div style="text-align: center">{{ elProps.fields[key].name }}</div>
      </el-col>
      <el-col :span="2">
        <div style="text-align: center">操作</div>
      </el-col>
    </el-row>
    <el-form :model="currentForm" ref="currentFormRef" label-width="0px" size="mini" type="flex">
      <el-row style="margin-bottom: 0" :gutter="5" v-for="(field, index) in currentForm.data" :key="index">
        <el-col :span="elProps.index.span" v-if="elProps.index">
          <div style="text-align: center">
            {{ index + 1 }}
          </div>
        </el-col>
        <el-col :span="elProps.fields[key].span" v-for="(_,key) in elProps.fields" :key="key">
          <el-form-item
            :prop="'data.' + index + '.' + key"
            :rules="[
                { required: elProps.fields[key].required, message: '不能为空', trigger: 'blur' },
              ]"
            style="text-align: center"
          >
            <el-select v-model="field[key]" v-if="elProps.fields[key].type === 'select'" placeholder="请选择">
              <el-option
                v-for="item in elProps.fields[key].option"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
            <el-input-number style="width: 100%" v-else-if="elProps.fields[key].type === 'number'"
                             controls-position="right" v-model="field[key]"></el-input-number>
            <div class="d2p-images" v-else-if="elProps.fields[key].type === 'image'">
              <d2p-file-uploader v-model="field[key]"
                                 :elProps="elProps.fields[key].elProps || { listType: 'picture-card', accept: '.png,.jpeg,.jpg,.ico,.bmp,.gif', limit: 1 }"></d2p-file-uploader>
            </div>
            <!--     富文本     -->
            <span v-else-if="elProps.fields[key].type === 'ueditor'">
              <values-popover v-model="field[key]" :elProps="{ type: 'ueditor' }"
                              @previewClick="previewClick(index,key)"></values-popover>
            </span>
            <!--     多对多     -->
            <span v-else-if="elProps.fields[key].type === 'many_to_many'">
              <values-popover
                v-model="field[key]"
                :dict="elProps.fields[key].dict"
                :elProps="{ type: elProps.fields[key].value?.type || 'manyToMany',  rowKey: elProps.fields[key].value?.rowKey || 'title', label: elProps.value?.title || '答复选项内容' }"
                @listClick="manyToManyClick(index,key)">
              </values-popover>
            </span>
            <el-input v-model="field[key]" v-else placeholder="请输入"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="4">
          <el-form-item>
            <el-button @click.prevent="topDomain(index)" :disabled="index === 0" type="primary" circle
                       icon="el-icon-top"></el-button>
            <el-button @click.prevent="bottomDomain(index)" :disabled="index === currentForm.data.length - 1"
                       type="primary" circle icon="el-icon-bottom"></el-button>
            <el-button @click.prevent="removeDomain(index)" type="danger" circle icon="el-icon-delete"></el-button>
          </el-form-item>
        </el-col>
      </el-row>
      <el-form-item>
        <el-col :span="12">
          <el-button type="primary" @click="addDomain">新增</el-button>
        </el-col>
      </el-form-item>
    </el-form>
    <el-dialog
      title="富文本内容编辑"
      :visible.sync="previewVisible"
      append-to-body
      width="900">
      <d2p-ueditor
        v-if="currentForm.data && currentForm.data[ueditorIndex] && ueditorKey"
        v-model="currentForm.data[ueditorIndex][ueditorKey]"
        :config="ueditorConfig">
      </d2p-ueditor>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="previewVisible = false">完成</el-button>
      </span>
    </el-dialog>
    <el-dialog
      title="编辑"
      :visible.sync="manyToManyVisible"
      append-to-body
      v-if="currentForm.data && currentForm.data[manyToManyIndex] && manyToManyKey"
      :width="elProps.fields[manyToManyKey].dialogWidth">
      <foreign-key-crud-form
        v-model="currentForm.data[manyToManyIndex][manyToManyKey]"
        :isInitRows="elProps.fields[manyToManyKey].isInitRows"
        :elProps="elProps.fields[manyToManyKey].elProps"
        @change="foreignChange"
      ></foreign-key-crud-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="manyToManyVisible = false">保存</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
import util from '@/libs/util.js'

export default {
  name: 'foreignKeyCrudForm',
  model: {
    prop: 'value',
    event: ['change', 'input']
  },
  props: {
    elProps: {
      type: Object,
      default () {
        return {
          isInitRows: true, // 是否初始化一行
          index: {
            name: '序号',
            span: 2
          },
          fields: {
            description: {
              name: '内容描述',
              type: 'input',
              span: 10,
              default: null,
              required: true
            },
            content: {
              name: '类型',
              type: 'select',
              span: 4,
              default: 0,
              required: true,
              options: [{
                value: '0',
                label: '单选项'
              }, {
                value: '1',
                label: '多选项'
              }, {
                value: '2',
                label: '单行填空'
              }, {
                value: '3',
                label: '多行填空'
              }]
            },
            score: {
              name: '分数',
              type: 'number',
              span: 4,
              default: 0,
              required: true,
              min: 0,
              max: null
            },
            option_data: {
              name: '选项题目',
              type: 'many_to_many',
              span: 2,
              default: [],
              required: false,
              unit: '个',
              value: {
                type: 'strList',
                rowKey: 'name',
                title: '选项内容'
              },
              // 子级多对多
              isInitRows: true,
              dialogWidth: '700',
              dict: {
                value: 'id', // 数据字典中value字段的属性名
                label: 'name' // 数据字典中label字段的属性名
              },
              elProps: {
                index: {
                  name: '序号',
                  span: 2
                },
                fields: {
                  name: {
                    name: '题目选项内容',
                    type: 'input',
                    span: 10,
                    default: null,
                    required: true
                  },
                  sort: {
                    name: '排序',
                    type: 'number',
                    span: 8,
                    default: 0,
                    required: true,
                    min: 0,
                    max: null
                  }
                }
              }
            }
          }
        }
      }
    },
    value: {
      type: Array,
      required: false
    }
  },
  data () {
    return {
      ueditorConfig: {
        serverUrl: util.baseURL() + 'api/system/file/ueditor/',
        headers: { Authorization: 'JWT ' + util.cookies.get('token') },
        imageUrlPrefix: util.baseFileURL(),
        // 涂鸦图片上传
        scrawlUrlPrefix: util.baseFileURL(),
        // 截图工具上传
        snapscreenUrlPrefix: util.baseFileURL(),
        // 抓取远程图片路径前缀
        catcherUrlPrefix: util.baseFileURL(),
        // 视频访问路径前缀
        videoUrlPrefix: util.baseFileURL(),
        // 文件访问路径前缀
        fileUrlPrefix: util.baseFileURL(),
        // 列出指定目录下的图片
        imageManagerUrlPrefix: util.baseFileURL(),
        // 列出指定目录下的文件
        fileManagerUrlPrefix: util.baseFileURL()
        // 传入ueditor的配置
        // 文档参考： http://fex.baidu.com/ueditor/#start-config
      },
      // 富文本弹窗编辑框
      previewVisible: false,
      ueditorIndex: 0,
      ueditorKey: null,
      // 多对多弹窗
      manyToManyIndex: 0,
      manyToManyKey: null,
      manyToManyVisible: false
    }
  },
  computed: {
    // eslint-disable-next-line vue/return-in-computed-property
    submitForm () {
      let res = ''
      this.$refs.currentFormRef.validate((valid) => {
        if (valid) {
          const { data } = this.currentForm
          res = data
        } else {
          console.log('error submit!!')
          return false
        }
      })
      return res
    },
    currentForm () {
      if (!this.value || !this.value[0]) {
        if (this.elProps.isInitRows) {
          const fields = {
            _id: this.value?.length || 0
          }
          for (const key in this.elProps.fields) {
            fields[key] = this.elProps.fields[key].default || null
          }
          this.$emit('change', [fields])
          this.$emit('input', [fields])
          return {
            data: [fields]
          }
        } else {
          return {
            data: []
          }
        }
      }
      return {
        data: this.value
      }
    }
  },
  created () {
  },
  methods: {
    // 数组元素互换位置，并且替换顺序
    swapArray (arr, index1, index2) {
      arr[index1] = arr.splice(index2, 1, arr[index1])[0]
      arr[index2].sort = index2 + 1
      arr[index1].sort = index1 + 1
      return arr
    },
    // 删除
    removeDomain (index) {
      this.currentForm.data.splice(index, 1)
      this.$emit('change', this.currentForm.data)
      this.$emit('input', this.currentForm.data)
    },
    // 上移
    topDomain (index) {
      this.swapArray(this.currentForm.data, index - 1, index)
      this.$emit('change', this.currentForm.data)
      this.$emit('input', this.currentForm.data)
    },
    // 下移
    bottomDomain (index) {
      this.swapArray(this.currentForm.data, index, index + 1)
      this.$emit('change', this.currentForm.data)
      this.$emit('input', this.currentForm.data)
    },
    // 新增
    addDomain () {
      const fields = {
        _id: this.value?.length || 0
      }
      for (const key in this.elProps.fields) {
        fields[key] = this.elProps.fields[key].default || null
      }
      fields.sort = (this.value?.length || 0) + 1
      this.currentForm.data.push(fields)
      this.$emit('change', this.currentForm.data)
      this.$emit('input', this.currentForm.data)
    },
    // 富文本预览按钮点击事件
    previewClick (index, key) {
      this.ueditorIndex = index
      this.ueditorKey = key
      this.previewVisible = true
      console.log('previewClick', index, key)
    },
    // 多对多点击事件
    manyToManyClick (index, key) {
      this.manyToManyIndex = index
      this.manyToManyKey = key
      this.manyToManyVisible = true
      if (!this.currentForm.data[this.manyToManyIndex][this.manyToManyKey]) {
        this.currentForm.data[this.manyToManyIndex][this.manyToManyKey] = []
      }
    },
    foreignChange (res) {
      if (this.manyToManyKey) {
        this.currentForm.data[this.manyToManyIndex][this.manyToManyKey] = res
      }
    }
  }
}
</script>
<style lang="scss">
.d2p-images {
  height: 30px;
  width: 30px;

  .el-upload-list__item-thumbnail {
    height: 60px !important;
    width: 60px !important;
  }

  .el-upload-list__item {
    width: 60px !important;
    height: 60px !important;
    line-height: 0 !important;

    img {
      height: 60px !important;
      width: 60px !important;
    }
  }

  .el-upload-list__item-actions {
    height: 60px !important;
    width: 60px !important;
    line-height: 0 !important;
  }
}

</style>
<style lang="scss" scoped>
::v-deep .d2p-file-uploader .el-upload--picture-card {
  width: 50px;
  height: 50px;
}
</style>
