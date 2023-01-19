<template>
  <TaskCom />
</template>

<script>
import Vue from 'vue'
import TaskCom from './task/index.vue'
import { install } from './component/index'

export default {
  name: 'TimingTask',

  components: {
    TaskCom
  },

  created () {
    install(Vue)
  }
}
</script>
