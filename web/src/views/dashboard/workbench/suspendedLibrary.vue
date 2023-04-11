<template>
  <div>
    <div class="sssss">
      <div
        class="callback float"
        @click="onClick"
        ref="fu"
      >
        <slot name="callbackButton"/>
      </div>
      <div
        style="right: 0;position: fixed;bottom: 0;"
        v-if="menu"
        class="menuclass"
      >
        <div class="titlea">
          添加部件 <i style="color: #409eff" class="el-icon-plus"></i>
          <span class="operateCallback">
            <slot name="operateButton"/>
          </span>
        </div>
        <slot name="widgetsList"/>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'suspendedLibrary',

  data () {
    return {
      menu: false,
      isLoading: false,
      background: [
        'linear-gradient(150deg, #accaff 0%, #3b88ec 100%)',
        'linear-gradient(150deg, #c5f8e6 0%, #10a465 100%)',
        'linear-gradient(150deg, #e8d6ff 0%, #9f55ff 100%)',
        'linear-gradient(150deg, #fdda45 0%, #fe6b62 100%)',
        'linear-gradient(150deg, #cefbc8 0%, #00aec5 100%)',
        'linear-gradient(150deg, #c5f8e6 0%, #10a465 100%)'
      ]
    }
  },
  created () {
  },
  mounted () {
  },
  methods: {
    onClick () {
      this.$emit('click')
    }
  }
}
</script>
<style scoped>
.callback p {
  font-size: 16px;
  color: #fff;
  background: rgba(56, 57, 58, 0.5);
  border-radius: 50%;
  text-align: center;
  width: 50px;
  height: 50px;
  line-height: 50px;
  font-family: PingFang SC;
  font-weight: 600;
  box-shadow: 0 0 10px #fff;
}
.callback img {
  display: block;
  width: 50px;
  height: 50px;
  box-shadow: 0 0 10px rgb(133, 129, 129);
  border-radius: 50%;
  background: #fff;
}
.operateCallback {
  position: fixed;
  height: 40px;
  right: 10px;
  z-index: 99999;
}
.callback {
  position: fixed;
  width: 40px;
  height: 40px;
  background-repeat: no-repeat;
  background-size: 100% 100%;
  bottom: 55px;
  right: 45px;
  z-index: 99999;
}
.float {
  position: fixed;
  touch-action: none;
  text-align: center;
  border-radius: 24px;
  line-height: 48px;
  color: white;
}

.menuclass {
  text-align: left;
  position: absolute;
  color: #000;
  width: 764px;
  background: #ffffff;
  box-shadow: 0px 6px 26px 1px rgba(51, 51, 51, 0.16);
  padding: 20px;
}
.sssss {
  position: relative;
  background-color: #000;
  right: 0;
  z-index: 100;
}
.titlea {
  font-size: 18px;
  font-family: Microsoft YaHei-Bold, Microsoft YaHei;
  font-weight: bold;
  color: #333333;
}
</style>
