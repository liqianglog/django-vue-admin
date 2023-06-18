<!-- 多对多value值展示组件 -->
<template>
  <div>
    <el-popover
      placement="right"
      width="400"
      trigger="hover"
      v-if="value.length > 0"
      @show="showEvents">
      <el-descriptions class="margin-top" :column="1" size="mini" border>
<!--        <template slot="extra">-->
<!--          <el-button type="primary" size="mini" disabled>上一页</el-button>-->
<!--          <el-button type="primary" size="mini" disabled>下一页</el-button>-->
<!--        </template>-->
        <el-descriptions-item v-for="(item,index) in data" :key="index">
          <template slot="label">
            <i class="el-icon-user"></i>
            {{ elProps.label }}
          </template>
          {{ item[dict.label] }}
        </el-descriptions-item>
      </el-descriptions>
      <el-button type="primary" plain size="mini" slot="reference"><span> {{ value.length }} {{elProps.unit}}</span>
      </el-button>
    </el-popover>
    <el-button v-else type="primary" plain size="mini" slot="reference"><span> {{ value.length }} {{elProps.unit}}</span>
      </el-button>
  </div>
</template>

<script>
import { d2CrudPlus } from 'd2-crud-plus'
import { request } from '@/api/service'

export default {
  name: 'm2m-values-popover',
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
          type: 'text', // test/tree
          rowKey: 'users',
          label: '标题',
          unit: '个'
        }
      }
    }
  },
  data () {
    return {
      data: []
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
      if (!this.data[0]) {
        this.getData()
      }
    },
    getData () {
      const params = {}
      params[this.dict.value] = this.value
      params.query = `{${this.dict.value},${this.dict.label}}`
      request({ url: this.dict.url, params: params }).then(ret => {
        this.data = ret.data.data || ret.data
      })
    }
  }
}
</script>
<style scoped>

</style>
