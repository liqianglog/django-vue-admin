<!-- value值展示组件 -->
<template>
  <div>
    <div v-if="elProps.type === 'list'">
      <el-popover
        placement="right"
        width="300"
        trigger="hover"
        v-if="value.length > 0"
        @show="showEvents"
        @hide="show=false">
        <el-descriptions class="margin-top" :column="1" size="mini" border>
          <el-descriptions-item v-for="(item,index) in data" :key="index">
            <template slot="label">
              <i class="el-icon-user"></i>
              {{ elProps.label }}
            </template>
            {{ item[dict.label] }}
          </el-descriptions-item>
        </el-descriptions>
        <el-button type="primary" plain size="mini" slot="reference" @click="listClick"><span> {{ value.length }} {{ elProps.unit }}</span>
        </el-button>
      </el-popover>
      <el-button v-else type="primary" plain size="mini" slot="reference" @click="listClick"><span> {{
          value.length
        }} {{ elProps.unit }}</span>
      </el-button>
    </div>
    <div v-if="elProps.type === 'strList'">
      <el-descriptions class="margin-top" :column="1" size="mini" border>
        <el-descriptions-item v-for="(item,index) in value" :key="index" labelStyle="width: 60px;">
          <template slot="label">
            选项{{ index + 1 }}
          </template>
          {{ item[dict.label] }}
        </el-descriptions-item>
      </el-descriptions>
    </div>
    <div v-if="elProps.type === 'manyToMany'">
     <el-popover
        placement="right"
        width="300"
        trigger="hover"
        v-if="value.length > 0"
        @show="showEvents"
        @hide="show=false">
        <el-descriptions class="margin-top" :column="1" size="mini" border>
          <el-descriptions-item v-for="(item,index) in value" :key="index" labelStyle="width: 60px;">
            <template slot="label">
              选项{{ index + 1 }}
            </template>
            {{ item[dict.label] }}
          </el-descriptions-item>
        </el-descriptions>
        <el-button type="primary" plain size="mini" slot="reference" @click="listClick"><span> {{ value.length }} {{ elProps.unit }}</span>
        </el-button>
      </el-popover>
      <el-button v-else type="primary" plain size="mini" slot="reference" @click="listClick"><span> {{
          value.length
        }} {{ elProps.unit }}</span>
      </el-button>
    </div>
    <div v-else-if="elProps.type === 'ueditor'">
      <el-popover
        placement="right"
        width="400"
        trigger="hover"
        v-if="value && value.length > 0"
        popper-class="userprjtreepop"
        @show="showEvents"
        @hide="show=false">
        <div v-html="value" v-if="show"></div>
        <el-button type="primary" plain size="mini" slot="reference" @click="previewClick"><span>预览</span>
        </el-button>
      </el-popover>
      <el-button v-else type="primary" plain size="mini" slot="reference" @click="previewClick"><span>预览</span>
      </el-button>
    </div>
  </div>
</template>

<script>
import { d2CrudPlus } from 'd2-crud-plus'
import { request } from '@/api/service'

export default {
  name: 'valuesPopover',
  model: {
    prop: 'value',
    event: ['change', 'input']
  },
  mixins: [d2CrudPlus.input, d2CrudPlus.inputDict],
  props: {
    // 值
    value: {
      type: [String, Number, Array],
      required: false,
      default: ''
    },
    // 数据字典配置
    dict: {
      type: Object,
      require: true
    },
    // 其他配置
    elProps: {
      type: Object,
      require: false,
      default () {
        return {
          type: 'text', // test/tree/list/ueditor
          rowKey: 'users',
          label: '标题',
          unit: '个'
        }
      }
    }
  },
  data () {
    return {
      data: [],
      show: false
    }
  },
  value: {
    handler (value, oldVal) {
      this.showEvents()
    },
    deep: true
  },
  computed: {
    _elProps () {
      return this.elProps
    }
  },
  mounted () {
  },
  methods: {
    showEvents () {
      this.show = true
      if (this.elProps.type === 'list') {
        if (!this.data[0]) {
          this.getListData()
        }
      }
    },
    getListData () {
      const params = {}
      if (this.value.constructor === Array) {
        const ids = []
        this.value.map(res => {
          if (res) {
            ids.push(res[this.dict.value])
          }
        })
        params[this.dict.value] = ids
      } else {
        params[this.dict.value] = this.value
      }
      params.query = `{${this.dict.value},${this.dict.label}}`
      request({ url: this.dict.url, params: params }).then(ret => {
        this.data = ret.data.data || ret.data
      })
    },
    previewClick () {
      this.$emit('previewClick')
    },
    listClick () {
      this.$emit('listClick')
    }
  }
}
</script>
<style>
.userprjtreepop {
  width: 80%;
  overflow-x: auto;
  max-height: 80%;
  overflow-y: auto;
}
</style>
