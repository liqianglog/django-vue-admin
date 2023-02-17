<template>
  <d2-container>
    <div :class="['widgets-home', customizing?'customizing':'']" ref="main">
      <div class="widgets-content">
        <div class="widgets-top">
          <div class="widgets-top-title">
            控制台
          </div>
          <div class="widgets-top-actions">
            <el-button v-if="customizing" type="primary" icon="el-icon-check" round @click="save">完成</el-button>
            <el-button v-else type="primary" icon="el-icon-edit" round @click="custom">自定义</el-button>
          </div>
        </div>
        <div class="widgets" ref="widgets">
          <div class="widgets-wrapper">
            <div v-if="nowCompsList.length<=0" class="no-widgets">
              <el-empty image="img/no-widgets.svg" description="没有部件啦" :image-size="280"></el-empty>
            </div>
            <grid-layout :layout.sync="layout"
                         :col-num="24"
                         :row-height="10"
                         :is-draggable="customizing"
                         :vertical-compact="false"
                         :use-css-transforms="true"
                         :use-row-transforms="true"
                         :autoSize="true"
                         :preventCollision="true"
            >
              <grid-item v-for="(item, index) in layout"
                         :static="item.static"
                         :x="item.x"
                         :y="item.y"
                         :w="item.w"
                         :h="item.h"
                         :i="item.i"
                         :key="index"
                         :isResizable="false"
              >
                <component :is="allComps[item.element]"></component>
                <div v-if="customizing" class="customize-overlay">
                  <el-button class="close" type="danger" plain icon="el-icon-close" size="small"
                             @click="remove(index)"></el-button>
                  <label>
                    <i :class="allComps[item.element].icon"></i>
                    {{ allComps[item.element].title }}</label>
                </div>
              </grid-item>
            </grid-layout>
          </div>
        </div>
      </div>
      <div v-if="customizing" class="widgets-aside">
        <el-container>
          <el-header>
            <div class="widgets-aside-title">
              <el-icon>
                <el-icon-circle-plus-filled/>
              </el-icon>
              添加部件
            </div>
            <div class="widgets-aside-close" @click="close()">
              <el-icon>
                <el-icon-close/>
              </el-icon>
            </div>
          </el-header>
          <el-main class="nopadding">
            <div class="widgets-list">
              <div v-if="myCompsList.length<=0" class="widgets-list-nodata">
                <el-empty description="没有部件啦" :image-size="60"></el-empty>
              </div>
              <div v-for="item in myCompsList" :key="item.title" class="widgets-list-item">
                <div class="item-logo">
                  <i :class="item.icon"></i>
                </div>
                <div class="item-info">
                  <h2>{{ item.title }}</h2>
                  <p>{{ item.description }}</p>
                </div>
                <div class="item-actions">
                  <el-button type="primary" icon="el-icon-plus" size="small" @click="push(item)"></el-button>
                </div>
              </div>
            </div>
          </el-main>
          <el-footer style="height:51px;">
            <el-button size="small" @click="backDefaul()">恢复默认</el-button>
          </el-footer>
        </el-container>
      </div>
    </div>

  </d2-container>
</template>

<script>
import draggable from 'vuedraggable'
import allComps from './components'
import util from '@/libs/util'
import VueGridLayout from 'vue-grid-layout'

export default {
  components: {
    draggable,
    GridLayout: VueGridLayout.GridLayout,
    GridItem: VueGridLayout.GridItem
  },
  data() {
    return {
      customizing: false,
      allComps: allComps,
      selectLayout: [],
      defaultGrid: {
        // 默认分栏数量和宽度 例如 [24] [18,6] [8,8,8] [6,12,6]
        layout: [12, 6, 6],
        // 小组件分布，com取值:views/home/components 文件名
        copmsList: [
          ['welcome'],
          ['about', 'ver'],
          ['time', 'progress']
        ]
      },
      defaultLayout: [],
      layout: [
        // { x: 0, y: 0, w: 2, h: 2, i: '0', element: 'welcome' },
        // { x: 2, y: 0, w: 2, h: 4, i: '1', element: 'about' },
        // { x: 4, y: 0, w: 2, h: 5, i: '2', element: 'time' },
        // { x: 6, y: 0, w: 2, h: 3, i: '3', element: 'progress' }
      ]
    }
  },
  created() {
    this.layout = JSON.parse(util.cookies.get('grid-layout') || JSON.stringify(this.defaultLayout))
  },
  mounted() {
    this.$emit('on-mounted')
  },
  computed: {
    allCompsList() {
      var allCompsList = []
      for (var key in this.allComps) {
        allCompsList.push({
          key: key,
          title: allComps[key].title,
          icon: allComps[key].icon,
          height: allComps[key].height,
          width: allComps[key].width,
          maxH: allComps[key].maxH || Infinity,
          maxW: allComps[key].maxW || Infinity,
          isResizable: allComps[key].isResizable || null,
          description: allComps[key].description
        })
      }
      return allCompsList
    },
    myCompsList() {
      return this.allCompsList
    },
    nowCompsList() {
      return this.allCompsList
    }
  },
  methods: {
    // 开启自定义
    custom() {
      this.customizing = true
      const oldWidth = this.$refs.widgets.offsetWidth
      this.$nextTick(() => {
        const scale = this.$refs.widgets.offsetWidth / oldWidth
        this.$refs.widgets.style.setProperty('transform', `scale(${scale})`)
      })
    },
    // 设置布局
    setLayout(layout) {
      // 暂定
    },
    getLayoutElementNumber(elementName) {
      var index = 0
      this.layout.map(res => {
        if (elementName === res.element) {
          index += 1
        }
      })
      return index + 1
    },
    // 追加
    push(item) {
      console.log(1, item)
      this.layout.push({
        x: 6,
        y: 0,
        w: item.width,
        h: item.height,
        maxH: item.maxH || Infinity,
        maxW: item.maxW || Infinity,
        isResizable: item.isResizable || null,
        i: item.key + this.getLayoutElementNumber(item.key),
        element: item.key
      })
    },
    // 删除组件
    remove(index) {
      this.layout.splice(index, 1)
    },
    // 保存
    save() {
      console.log(this.layout)
      this.customizing = false
      this.$refs.widgets.style.removeProperty('transform')
      util.cookies.set('grid-layout', this.layout)
    },
    // 恢复默认
    backDefaul() {
      this.customizing = false
      this.$refs.widgets.style.removeProperty('transform')
      this.layout = JSON.parse(JSON.stringify(this.defaultLayout))
      util.cookies.remove('grid-layout')
    },
    // 关闭
    close() {
      this.customizing = false
      this.$refs.widgets.style.removeProperty('transform')
    }
  }
}
</script>
<style scoped lang="scss">
.widgets-home {
  display: flex;
  flex-direction: row;
  flex: 1;
  height: 100%;
}

.widgets-content {
  flex: 1;
  overflow: auto;
  overflow-x: hidden;
  padding: 15px;
}

.widgets-aside {
  width: 360px;
  background: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, .1);
  position: relative;
  overflow: auto;
}

.widgets-aside-title {
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.widgets-aside-title i {
  margin-right: 10px;
  font-size: 18px;
}

.widgets-aside-close {
  font-size: 18px;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 3px;
  cursor: pointer;
}

.widgets-aside-close:hover {
  background: rgba(180, 180, 180, 0.1);
}

.widgets-top {
  margin-bottom: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.widgets-top-title {
  font-size: 18px;
  font-weight: bold;
}

.widgets {
  transform-origin: top left;
  transition: transform .15s;
}

.draggable-box {
  height: 100%;
}

.customizing .widgets-wrapper {
  margin-right: -360px
}

.customizing .widgets-wrapper .el-col {
  padding-bottom: 15px;
}

.customizing .widgets-wrapper .draggable-box {
  border: 1px dashed #409EFF;
  padding: 15px;
}

.customizing .widgets-wrapper .no-widgets {
  display: none;
}

.customizing .widgets-item {
  position: relative;
  margin-bottom: 15px;
}

.customize-overlay {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.5);
  cursor: move;
}

.customize-overlay label {
  background: #409EFF;
  color: #fff;
  height: 40px;
  padding: 0 30px;
  border-radius: 40px;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: move;
}

.customize-overlay label i {
  margin-right: 15px;
  font-size: 24px;
}

.customize-overlay .close {
  position: absolute;
  top: 15px;
  right: 15px;
}

.customize-overlay .close:focus, .customize-overlay .close:hover {
  background: #76B1F9;
}

.widgets-list {
}

.widgets-list-item {
  display: flex;
  flex-direction: row;
  padding: 15px;
  align-items: center;
}

.widgets-list-item .item-logo {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(180, 180, 180, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  margin-right: 15px;
  color: #6a8bad;
}

.widgets-list-item .item-info {
  flex: 1;
}

.widgets-list-item .item-info h2 {
  font-size: 16px;
  font-weight: normal;
  cursor: default;
}

.widgets-list-item .item-info p {
  font-size: 12px;
  color: #999;
  cursor: default;
}

.widgets-list-item:hover {
  background: rgba(180, 180, 180, 0.1);
}

.widgets-wrapper .sortable-ghost {
  opacity: 0.5;
}

.selectLayout {
  width: 100%;
  display: flex;
}

.selectLayout-item {
  width: 60px;
  height: 60px;
  border: 2px solid #EBEEF5;
  padding: 5px;
  cursor: pointer;
  margin-right: 15px;
}

.selectLayout-item span {
  display: block;
  background: #EBEEF5;
  height: 46px;
}

.selectLayout-item.item02 span {
  height: 30px;
}

.selectLayout-item.item02 .el-col:nth-child(1) span {
  height: 14px;
  margin-bottom: 2px;
}

.selectLayout-item.item03 span {
  height: 14px;
  margin-bottom: 2px;
}

.selectLayout-item:hover {
  border-color: #409EFF;
}

.selectLayout-item.active {
  border-color: #409EFF;
}

.selectLayout-item.active span {
  background: #409EFF;
}

.dark {
  .widgets-aside {
    background: #2b2b2b;
  }

  .customize-overlay {
    background: rgba(43, 43, 43, 0.9);
  }
}

@media (max-width: 992px) {
  .customizing .widgets {
    transform: scale(1) !important;
  }
  .customizing .widgets-aside {
    width: 100%;
    position: absolute;
    top: 50%;
    right: 0;
    bottom: 0;
  }
  .customizing .widgets-wrapper {
    margin-right: 0;
  }
}

.customizing {
  .vue-grid-layout {
    background: #eee;
  }

  .vue-grid-item:not(.vue-grid-placeholder) {
    background: #ccc;
    border: 1px solid black;
  }

  .vue-grid-item .resizing {
    opacity: 0.9;
  }

  .vue-grid-item .static {
    background: #cce;
  }

  .vue-grid-item .text {
    font-size: 24px;
    text-align: center;
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    margin: auto;
    height: 100%;
    width: 100%;
  }

  .vue-grid-item .no-drag {
    height: 100%;
    width: 100%;
  }

  .vue-grid-item .minMax {
    font-size: 12px;
  }

  .vue-grid-item .add {
    cursor: pointer;
  }

  .vue-draggable-handle {
    position: absolute;
    width: 20px;
    height: 20px;
    top: 0;
    left: 0;
    background: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10'><circle cx='5' cy='5' r='5' fill='#999999'/></svg>") no-repeat;
    background-position: bottom right;
    padding: 0 8px 8px 0;
    background-repeat: no-repeat;
    background-origin: content-box;
    box-sizing: border-box;
    cursor: pointer;
  }
}
</style>
