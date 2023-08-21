<template>
  <el-dropdown size="small" class="d2-mr">
    <el-link
      type="primary"
      :underline="false"
      style="margin-bottom: 2px;margin-left: 10px"
      v-if="isTenants"
      >
      <span>
        当前租户：{{info.tenant_name}}
      </span>
      <span style="color: #E6A23C;" v-if="info.tenant_id && info.tenant_id !== 100000" @click="clientInfo">
        切换套餐
      </span>
      <span class="btn-text">{{
      info.name ? `你好 ${info.name}` : "未登录"
    }}</span>
    </el-link>
    <span class="btn-text" v-else>{{
      info.name ? `你好 ${info.name}` : "未登录"
    }}</span>
    <el-dropdown-menu slot="dropdown">
      <el-dropdown-item @click.native="userInfo">
        <d2-icon name="cog" class="d2-mr-5" />个人信息
      </el-dropdown-item>
      <el-dropdown-item @click.native="clientInfo" v-if="info.tenant_id && info.tenant_id !== 100000">
        <d2-icon name="cog" class="d2-mr-5" />租户信息
      </el-dropdown-item>
      <el-dropdown-item @click.native="logOff" divided>
        <d2-icon name="power-off" class="d2-mr-5" />
        注销
      </el-dropdown-item>
    </el-dropdown-menu>
    <el-image v-if="info.avatar" :src="info.avatar" :preview-src-list="[info.avatar]" style="width: 20px;height: 20px;border-radius: 20%;top: 5px;" alt="头像"></el-image>
  </el-dropdown>
</template>

<script>
import { mapState, mapActions } from 'vuex'
export default {
  computed: {
    ...mapState('d2admin/user', ['info'])
  },
  data () {
    return {
      isTenants: window.pluginsAll && window.pluginsAll.indexOf('dvadmin-tenants-web') !== -1
    }
  },
  methods: {
    ...mapActions('d2admin/account', ['logout']),
    /**
     * @description 登出
     */
    logOff () {
      this.logout({
        confirm: true
      })
    },
    /** 个人信息 */
    userInfo () {
      this.$router.push({ path: 'userInfo' })
    },
    /** 租户信息 */
    clientInfo () {
      this.$router.push({ path: 'myClientInfo' })
    }
  }
}
</script>
