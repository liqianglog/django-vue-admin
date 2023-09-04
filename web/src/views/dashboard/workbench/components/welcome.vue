<template>
  <el-card
    shadow="hover"
    :header="config?.showHeader?.value ? '欢迎使用' : ''"
    class="card-view"
    :style="{background: randomColor(), color: config?.fontColor?.value}">
    <div class="welcome">
      <div class="logo">
        <img src="/image/django-vue-admin.png">
        <h2>欢迎体验 Dvadmin</h2>
      </div>
      <div class="tips">
        <div class="tips-item">
          <div class="tips-item-icon">
            <i class="el-icon-menu"></i>
          </div>
          <div class="tips-item-message">这里是项目控制台，你可以点击右上方的“自定义”按钮来添加移除或者移动部件。</div>
        </div>
        <div class="tips-item">
          <div class="tips-item-icon">
            <i class="el-icon-star-on"></i>
          </div>
          <div class="tips-item-message">热爱Python和Vue,打造一个低代码开源平台，并且持续着。</div>
        </div>
        <div class="tips-item">
          <div class="tips-item-icon">
            <i class="el-icon-milk-tea"></i>
          </div>
          <div class="tips-item-message">项目目的：让前端和后端工作更快乐</div>
        </div>
      </div>
      <div class="actions">
        <el-button type="primary" icon="el-icon-check" size="large" @click="godoc">文档</el-button>
      </div>
    </div>
  </el-card>
</template>

<script>
export default {
  sort: 11,
  title: '欢迎使用',
  name: 'welcome',
  icon: 'el-icon-present',
  description: '项目特色以及文档链接',
  width: 16,
  height: 45,
  isResizable: true,
  config: {
    showHeader: {
      label: '显示头部信息',
      type: 'boot',
      value: true,
      placeholder: '颜色为空则随机变换颜色'
    },
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
    return {}
  },
  methods: {
    godoc () {
      window.open('https://www.django-vue-admin.com/')
    },
    // 生成一个颜色
    randomColor () {
      if (this.config?.color?.value) {
        return this.config.color.value
      }
      return 'linear-gradient(150deg, #3b88ec 0%, #accaff 100%)'
    }
  }
}
</script>

<style scoped lang="scss">
.card-view {
  color: $color-primary;
}
.welcome .logo {
  text-align: center;
}

.welcome .logo img {
  vertical-align: bottom;
  width: 100px;
  height: 100px;
  margin-bottom: 20px;
}

.welcome .logo h2 {
  font-size: 30px;
  font-weight: normal;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tips {
  margin-top: 20px;
  padding: 0 40px;
}

.tips-item {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 7.5px 0;
}

.tips-item-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 18px;
  margin-right: 20px;
  color: var(--el-color-primary);
  background: rgba(180, 180, 180, 0.1);
}

.tips-item-message {
  flex: 1;
  font-size: 14px;
}

.actions {
  text-align: center;
  margin: 40rpx 0 20rpx 0;
}
.el-card{
  height: 100%;
}
</style>
