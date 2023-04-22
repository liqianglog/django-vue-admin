<template>
  <el-card shadow="hover" class="card-view" :style="{backgroundColor: randomColor(),color: config?.fontColor?.value}">
    <div class="time">
      <h2>{{ time }}</h2>
      <p>{{ day }}</p>
    </div>
  </el-card>
</template>

<script>
import dayjs from 'dayjs'

export default {
  sort: 12,
  title: '时钟',
  name: 'myTime',
  icon: 'el-icon-alarm-clock',
  description: '演示部件效果',
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
      time: '',
      day: ''
    }
  },
  mounted () {
    this.showTime()
    setInterval(() => {
      this.showTime()
    }, 1000)
  },
  methods: {
    showTime () {
      this.time = dayjs().format('HH:mm:ss')
      this.day = dayjs().format('YYYY年MM月DD日')
    },
    // 生成一个颜色
    randomColor () {
      if (this.config?.color?.value) {
        return this.config.color.value
      }
      return 'linear-gradient(to right, #8E54E9, #4776E6)'
    }
  }
}
</script>

<style scoped lang="scss">
.card-view {
  color: $color-primary;
}

.time h2 {
  font-size: 24px;
}

.time p {
  font-size: 18px;
  margin-top: 10px;
  opacity: 0.7;
}
::v-deep .el-card__body {
  height: 110px;

}
.el-card{
  height: 100%;
}
</style>
