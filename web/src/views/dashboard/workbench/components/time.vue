<template>
  <el-card shadow="hover" header="时钟" class="item-background">
    <div class="time">
      <h2>{{ time }}</h2>
      <p>{{ day }}</p>
    </div>
  </el-card>
</template>

<script>
import dayjs from 'dayjs'

export default {
  title: '时钟',
  icon: 'el-icon-alarm-clock',
  description: '演示部件效果',
  height: 17,
  minH: 17,
  width: 8,
  minW: 4,
  isResizable: true,
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
      this.time = dayjs().format('hh:mm:ss')
      this.day = dayjs().format('YYYY年MM月DD日')
    }
  }
}
</script>

<style scoped>
.item-background {
  background: linear-gradient(to right, #8E54E9, #4776E6);
  color: #fff;
}

.time h2 {
  font-size: 40px;
}

.time p {
  font-size: 14px;
  margin-top: 10px;
  opacity: 0.7;
}
</style>
