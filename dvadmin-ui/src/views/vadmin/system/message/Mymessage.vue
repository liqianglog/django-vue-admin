<template>
  <div class="app-container">
    <el-card shadow="never">
      <div class="message-page-con message-category-con">
        <el-menu
          default-active="1"
          class="el-menu-vertical-demo"
          @select="handleSelect">
          <el-menu-item index="1">
            <template slot="title">
              <span class="category-title">未读消息</span>
              <el-badge style="margin-bottom: 3px" :value="countUnread" :hidden="countUnread===0"></el-badge>
            </template>
          </el-menu-item>
          <el-menu-item index="2">
            <span class="category-title">已读消息</span>
            <el-badge style="margin-bottom: 3px" type="info" :value="countReaded"></el-badge>
          </el-menu-item>
        </el-menu>
      </div>
      <div class="message-page-con message-list-con">
        <el-menu
          default-active="2"
          class="el-menu-vertical-demo"
          @select="handleListSelect">
          <el-menu-item v-for="(item,index) in messageList" :key="index" :index="index.toString()">
            <template slot="title">
              <div style="line-height: 10px!important;height: 20px;">
                <p class="msg-title">{{ item.title }}</p>
                <el-badge is-dot class="item" :type="badgeType"></el-badge>
                {{item.create_datetime}}

              </div>
            </template>
          </el-menu-item>
        </el-menu>
      </div>
      <div class="message-page-con message-view-con">
        <div class="message-view-header">
          <h2 class="message-view-title">{{ showingMsgItem.title }}</h2>
          <time class="message-view-time">{{ showingMsgItem.create_datetime }}</time>
        </div>
        <div v-html="showingMsgItem.content"></div>
      </div>
    </el-card>
  </div>
</template>

<script>
  import {updateIsRead, userMessage} from "@/api/vadmin/system/message";
  import store from "@/store";

  export default {
    name: "Mymessage",
    data() {
      return {
        // 查询通知
        queryParams: {
          pageNum: 1,
          pageSize: 10,
        },
        messageList: [],
        // 已读通知
        countReaded: 0,
        messageReadedList: [],
        // 未读消息列表
        messageUnreadList: [],
        countUnread: 0,
        badgeType: 'danger',
        // 选中查询后的详细信息
        showingMsgItem: {}
      };
    },
    created() {
      this.getList()

    },
    methods: {
      /** 查询通知列表 */
      getList() {
        // 已读通知列表
        userMessage(this.addDateRange({...this.queryParams, is_read: 'True'})).then(response => {
            this.messageReadedList = response.data.results;
            this.countReaded = response.data.count;

          }
        );
        // 未读通知列表
        userMessage(this.addDateRange({...this.queryParams, is_read: 'False'})).then(response => {
            this.messageUnreadList = response.data.results;
            this.countUnread = response.data.count;
            this.messageList = this.messageUnreadList
          }
        );
      },
      handleSelect(key, keyPath) {
        this.messageList = key[0] === "1" ? this.messageUnreadList : this.messageReadedList
        this.badgeType = key[0] === "1" ? 'danger' : 'info'
      },
      // 通知列表激活后
      handleListSelect(key, keyPath) {
        this.showingMsgItem = this.messageList[key[0]]
        // 修改通知查询状态
        if (this.badgeType === "danger") {
          updateIsRead(this.showingMsgItem).then(response => {
            if(response.code === 200){
              store.commit('SET_UNREAD_MSG_COUNT', store.getters.unread_msg_count - 1);
              this.open = false;
              this.getList();
            }
          });
        }
      }
    }
  };
</script>
<style scoped>
  .app-container {
    background-color: #f5f7f9;
  }

  .message-category-con {
    border-right: 1px solid #e6e6e6;
    width: 200px;
  }

  .message-page-con {
    height: calc(100vh - 176px);
    display: inline-block;
    vertical-align: top;
    position: relative;
  }

  .category-title {
    display: inline-block;
    width: 65px;
  }


  .message-list-con {
    border-right: 1px solid #e6e6e6;
    width: 230px;
  }

  .msg-title {
    word-break: break-all;
    white-space: normal;
    line-height: 15px;
    color: rgb(170, 169, 169);
  }

  .message-list-con .el-menu-item {
    height: 80px;
    padding-top: 5px;
  }

  .item {
    margin-right: 10px;
    margin-bottom: 5px;
  }

  .message-view-con {
    position: absolute;
    left: 486px;
    top: 16px;
    right: 16px;
    bottom: 16px;
    overflow: auto;
    padding: 12px 20px 0;

  }

  .message-view-header {
    margin-bottom: 20px;

  }

  .message-view-title {
    display: inline-block;
  }

  .message-view-time {
    margin-left: 20px;
  }
</style>
