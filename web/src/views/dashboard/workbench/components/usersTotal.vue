<template>
  <el-card class="card-view" :style="{backgroundColor:randomColor(),color: config?.fontColor?.value}" shadow="always">
    <div>
      <el-row type="flex" justify="space-around" style="padding:10px">
        <el-col :span="12">
          <div class="card-content">
            <div class="card-content-label">用户总数</div>
            <div class="card-content-value">{{ usersTotal }}</div>
          </div>
        </el-col>
        <el-col :span="6" :offset="6" style="text-align: right;">
          <i class="el-icon-user-solid" size="48px"></i>
        </el-col>
      </el-row>
    </div>
  </el-card>
</template>

<script>
import { request } from '@/api/service'

export default {
  sort: 1,
  title: '用户总数',
  icon: 'el-icon-user-solid',
  description: '平台总会员数',
  name: 'usersTotal',
  height: 14,
  width: 16,
  isResizable: true,
  config: {
    color: {
      label: '背景颜色',
      type: 'color',
      value: '',
      placeholder: '颜色为空则随机变换颜色'
    },
    fontColor: {
      label: '字体颜色',
      type: 'color',
      value: '',
      placeholder: '请选择字体颜色'
    }
  },
  props: {
    config: {
      type: Object,
      required: false
    }
  },
  data () {
    return {
      usersTotal: ''
    }
  },
  methods: {
    initGet () {
      request({
        url: '/api/system/datav/users_total/'
      }).then((res) => {
        this.usersTotal = res.data.users_total
      })
    },
    // 生成一个随机整数
    randomColor () {
      if (this.config?.color?.value) {
        return this.config.color.value
      }
      return this.$util.randomColor()
    }
  },
  mounted () {
    this.initGet()
  }
}
</script>

<style scoped lang="scss">
.card-view {
  //border-radius: 10px;
  color: $color-primary;

  .card-content {
    .card-content-label {
      font-size: 1em;
    }

    .card-content-value {
      margin-top: 10px;
      font-size: 1.5em;
      font-weight: bold;
    }
  }
}

.el-icon-user-solid {
  font-size: 30px;
}

.el-card {
  height: 100%;
}
</style>
