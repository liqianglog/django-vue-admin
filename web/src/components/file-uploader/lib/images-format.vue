<template>
  <span class="d2p-image-format">
     <el-image
       :style="{width:imgWidth,height:imgHeight,'margin-right':'10px',border:'1px solid #eee'}"
       v-for="url in urls"  :key="url" :src="url"
       v-bind="_elProps" >
        <div slot="placeholder" class="image-slot">
            <img style="max-width:50%" src="./loading-spin.svg">
          </div>
       <template v-if="error==='slot'">
         <div slot="error" class="image-slot">
            <slot name="error"/>
         </div>
       </template>
       <template v-else-if="error">
         <div slot="error" class="image-slot">
            <img :src="error" width="50%"/>
         </div>
       </template>
     </el-image>
  </span>
</template>

<script>
// 图片行展示组件
export default {
  name: 'd2p-images-format',
  props: {
    // 图片的url
    // 'url' 或 ['url1','url2']
    value: {
      type: [String, Array],
      require: true
    },
    // 图片的宽度设置
    width: {
      require: false,
      default: 30
    },
    // 图片的高度设置
    height: {
      require: false,
      default: 30
    },
    fit: {
      default: 'contain'
    },
    // 内部封装[el-image](https://element.eleme.cn/#/zh-CN/component/image)组件的属性参数<br/>
    elProps: {
      type: Object
    },
    error: {
      default: undefined
    },
    // 构建下载url方法
    buildUrl: {
      type: Function,
      default: function (value, item) { return value }
    }
  },
  data () {
    return {
    }
  },
  computed: {
    urls () {
      const urls = []
      if (this.value == null || this.value === '') {
        return urls
      }
      if (typeof (this.value) === 'string') {
        urls.push(this.value)
      } else if (this.value instanceof Array) {
        for (const item of this.value) {
          if (item == null) {
            continue
          }
          if (item.url != null) {
            urls.push(item.url)
          } else {
            urls.push(item)
          }
        }
      } else {
        urls.push(this.value.url)
      }
      const arr = []
      for (const url of urls) {
        arr.push(this.buildUrl(url))
      }
      return arr
    },
    imgHeight () {
      if (typeof (this.height) === 'number') {
        return this.height + 'px'
      }
      return this.height
    },
    imgWidth () {
      if (typeof (this.width) === 'number') {
        return this.width + 'px'
      }
      return this.width
    },
    _elProps () {
      const defaultElProps = { fit: this.fit, previewSrcList: this.urls }
      Object.assign(defaultElProps, this.elProps)
      return defaultElProps
    }
  },
  mounted () {
  },
  methods: {
    handleClick () {
      // this.$emit('input', !this.value)
    }
  }
}
</script>
<style lang="scss">
.d2p-image-format{
  .image-slot{
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
  }
  .el-image-viewer__close {
    color: #fff;
  }
}

</style>
