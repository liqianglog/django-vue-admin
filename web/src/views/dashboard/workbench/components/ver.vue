<template>
  <el-card
    shadow="hover"
    :header="config?.showHeader?.value ? '版本信息' : ''"
    class="card-view"
    :style="{backgroundColor:randomColor(),color: config?.fontColor?.value}"
  >
    <div style="text-align: center;">
      <h2 style="margin-top: 5px;">{{ title }}</h2>
      <p style="margin-top: 5px;">最新版本 {{ ver }}</p>
    </div>
  </el-card>
</template>

<script>
import { mapState } from 'vuex'

export default {
  sort: 10,
  title: '版本信息',
  name: 'ver',
  icon: 'el-icon-monitor',
  description: '当前项目版本信息',
  height: 14,
  width: 16,
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
    return {
      ver: 'loading...',
      title: ''
    }
  },
  mounted () {
    this.getVer()
  },
  computed: {
    ...mapState('d2admin', {
      siteName: state => state.settings.data['login.site_name'] // 网站名称
    })
  },
  methods: {
    async getVer () {
      this.ver = `v${process.env.VUE_APP_VERSION}` || 'v2.1.1'
      this.title = this.siteName || process.env.VUE_APP_TITLE
    },
    // 生成一个颜色
    randomColor () {
      if (this.config?.color?.value) {
        return this.config.color.value
      }
      return this.$util.randomColor()
    }
  }
}
</script>
<style scoped lang="scss">
.card-view {
  color: $color-primary;
  //background: rgb(80,168,244);
  //box-shadow: 1px 6px 8px 2px rgba(80,168,244,0.2);
  .card-content {
    //text-align: center;
  }
}

::v-deep .el-card__body {
  height: 110px;

}

.el-card {
  height: 100%;
}
</style>
