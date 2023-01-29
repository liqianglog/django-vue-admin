<!--
 * @创建文件时间: 2021-11-24 21:05:26
 * @Auther: 猿小天
 * @最后修改人: 猿小天
 * @最后修改时间: 2021-12-30 13:53:20
 * 联系Qq:1638245306
 * @文件介绍:
-->
<template>
  <el-container
    style="
      background-color: #fff;
      margin-top: 20px;
      overflow-y: scroll;
      height: 52vh;
    "
  >
    <div>
      <el-timeline>
        <el-timeline-item
          v-for="(activity, index) in activities"
          :key="index"
          :icon="activity.icon"
          :type="activity.type"
          :color="activity.color"
          :size="activity.size"
          :timestamp="activity.timestamp"
        >
          {{ activity.content }}
        </el-timeline-item>
      </el-timeline>
    </div>
  </el-container>
</template>
<script>
import * as api from './../api'
import { mapState } from 'vuex'
export default {
  props: {
    options: {
      type: Object,
      default () {
        return {}
      }
    }
  },
  computed: {
    ...mapState('productionVuex', {
      brandOwnerOrderId: (state) => state.brandOwnerOrderId
    })
  },
  data () {
    return {
      activities: [],
      timer: null
    }
  },
  methods: {
    getInit () {
      if (this.options.mainId) {
        const params = {
          id: this.options.mainId,
          _fields: 'log,'
        }
        api.getObj(params).then((res) => {
          const { data } = res.data
          const activities = JSON.parse(data.log)
          this.activities = activities.reverse()
        })
      }
    }
  },
  mounted () {
    const that = this
    that.timer = setInterval(that.getInit, 3000)
  },
  created () {
    this.getInit()
  },
  beforeDestroy () {
    clearInterval(this.timer)
  }
}
</script>
