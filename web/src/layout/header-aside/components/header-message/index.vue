<template>
  <div>

    <el-tooltip
      effect="dark"
      content="通知"
      placement="bottom">
      <el-popover
        placement="bottom"
        width="400"
        trigger="click">
        <msg-list :msgObj="msgObj"></msg-list>
      <el-button
        class="d2-ml-0 d2-mr btn-text can-hover"
        type="text"
        slot="reference"  @click="getList">
        <d2-icon

          name="bell-o"
          style="font-size: 16px"/>
      </el-button>
    </el-popover>
    </el-tooltip>
  </div>
</template>

<script>
import msgList from './components/msg-list'
import { request } from '@/api/service'
export default {
  components:{
    msgList
  },
  data () {
    return {
      msgObj:null
    }
  },
  methods:{
    getList () {
      request({
        url: '/api/system/message_center/get_newest_msg/',
        method: 'get',
        params: {}
      }).then(res => {
        const {data} = res
        this.msgObj = data
      })
    }
  }
}
</script>
