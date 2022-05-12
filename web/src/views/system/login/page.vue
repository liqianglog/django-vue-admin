<template>
  <div
    class="w3l-signinform"
    :style="{
      background:
        'url(' +
        (loginBackground || require('./image/bg.jpg')) +
        ') no-repeat center'
    }"
  >
    <!-- container -->
    <div class="wrapper">
      <!-- main content -->
      <div class="w3l-form-info">
        <!-- logo -->
        <img class="page-login--logo" :src="siteLogo" width="300" />
        <div class="w3_info">
          <h2 style="text-align: center">{{ siteName || processTitle }}</h2>
          <el-card shadow="always" class="card">
            <el-tabs v-model="activeName">
              <el-tab-pane label="账号密码登录" name="first" stretch>
                <span slot="label"
                  ><span style="margin: 30px">账号密码登录</span></span
                >
                <br />
                <el-form
                  ref="loginForm"
                  label-position="top"
                  :rules="rules"
                  :model="formLogin"
                  size="default"
                >
                  <el-form-item prop="username">
                    <el-input
                      type="text"
                      v-model="formLogin.username"
                      prefix-icon="el-icon-user-solid"
                      placeholder="用户名"
                    >
                    </el-input>
                  </el-form-item>
                  <el-form-item prop="password">
                    <el-input
                      type="password"
                      v-model="formLogin.password"
                      prefix-icon="el-icon-s-promotion"
                      show-password
                      placeholder="密码"
                    >
                    </el-input>
                  </el-form-item>
                  <el-form-item prop="captcha">
                    <el-input
                      type="text"
                      v-model="formLogin.captcha"
                      placeholder="验证码"
                      @keyup.enter.native="submit"
                    >
                      <template slot="append">
                        <img
                          class="login-code"
                          height="33px"
                          width="145px"
                          slot="suffix"
                          :src="image_base"
                          @click="getCaptcha"
                        />
                      </template>
                    </el-input>
                  </el-form-item>
                </el-form>
                <button class="btn btn-primary btn-block" @click="submit">
                  登录
                </button>
              </el-tab-pane>
            </el-tabs>
          </el-card>

          <!-- footer -->
          <div class="footer">
            <p>Copyright &copy; {{ copyright }}</p>
            <p>
              <a href="https://beian.miit.gov.cn" target="_blank">{{
                keepRecord
              }}</a>
              | <a :href="helpUrl || '#'" target="_blank">帮助</a> |
              <a :href="privacyUrl || '#'" target="_blank">隐私</a> |
              <a :href="clauseUrl || '#'" target="_blank">条款</a>
            </p>
          </div>
          <!-- footer -->
        </div>
      </div>
      <!-- //main content -->
    </div>
    <!-- //container -->
  </div>
</template>
<script>
import base from './base.vue'

export default {
  extends: base,
  name: 'page',
  data () {
    return {
      activeName: 'first'
    }
  },
  created () {},
  mounted () {},
  methods: {}
}
</script>

<style lang="scss" scoped>
@import './css/style.css';

.copyrights {
  text-indent: -9999px;
  height: 0;
  line-height: 0;
  font-size: 0;
  overflow: hidden;
}
</style>
