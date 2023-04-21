<template>
  <el-card
    class="card-view"
    :style="{ backgroundColor: randomColor() }"
    shadow="always"
  >
    <div :style="{color: config?.fontColor?.value}">
      <div>
        <div class="card-content-label">数据库统计</div>
        <i class="real-time">实时</i>
      </div>
      <div class="absolute-left">
        <div class="card-content">
          <div class="card-content-value">{{ count }}</div>
          <div class="el-icon-coin">
            数据库数量
          </div>
        </div>
      </div>
      <div class="absolute-right">
        <div class="card-content-time">
          <div class="attachment-value">{{ space }}</div>
          <div class="el-icon-s-flag">
            占用空间
          </div>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script>
import { request } from '@/api/service'

export default {
  sort: 4,
  title: '数据库统计',
  name: 'databaseTotal',
  icon: 'el-icon-coin',
  description: '数据库统计',
  height: 14,
  width: 16,
  isResizable: true,
  data () {
    return {
      count: '',
      space: ''
    }
  },
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
  methods: {
    initGet () {
      request({
        url: '/api/system/datav/database_total/'
      }).then((res) => {
        this.count = res.data.count
        this.space = this.$util.formatBytes(res.data.space)
      })
    },
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
      font-size: 0.8em;
    }

    .card-content-value {
      margin-top: 5px;
      font-size: 1.5em;
      font-weight: bold;
    }
  }

  .attachment-value {
    margin-top: 5px;
    font-size: 1.5em;
    font-weight: bold;
  }

  .el-icon-coin {
    font-size: 12px;
  }

  .el-icon-s-flag {
    font-size: 12px;
  }
}

.real-time {
  background: rgb(53, 59, 86);
  color: #ffffff;
  font-size: 14px;
  font-style: normal;
  padding: 0 7px 0 7px;
  border-radius: 4px;
  position: absolute;
  right: 20px;
  top: 20px;
}

.el-card {
  height: 100%;
}
.absolute-right{
  position: absolute;
  right: 30px;
}
.absolute-left{
  position: absolute;
}
</style>
