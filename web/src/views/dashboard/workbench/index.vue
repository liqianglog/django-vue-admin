<template>
  <d2-container>
    <suspended-library ref="suspendedLibrary">
      <div class="set-btn-class" slot="callbackButton">
        <el-button v-if="customizing" type="primary" icon="el-icon-check" round @click="save">完成&nbsp;&nbsp;
        </el-button>
        <el-button v-else type="primary" icon="el-icon-edit" round @click="custom">自定义</el-button>
        <el-button v-if="minimize" type="warning" icon="el-icon-plus" round @click="clickMinimize">展开&nbsp;&nbsp;
        </el-button>
      </div>
      <div slot="operateButton">
        <el-tooltip class="item" effect="dark" content="清空画布" placement="top">
          <el-button v-if="customizing" type="danger" icon="el-icon-delete" circle size="mini"
                     @click="clickEmpty"></el-button>
        </el-tooltip>
        <el-tooltip class="item" effect="dark" content="最小化" placement="top">
          <el-button v-if="customizing" type="success" icon="el-icon-minus" circle size="mini"
                     @click="clickMinimize"></el-button>
        </el-tooltip>
        <el-tooltip class="item" effect="dark" content="恢复默认" placement="top">
          <el-button v-if="customizing" type="primary" icon="el-icon-refresh-right" circle size="mini"
                     @click="backDefault()"></el-button>
        </el-tooltip>
        <el-tooltip class="item" effect="dark" content="关闭" placement="top">
          <el-button v-if="customizing" type="danger" icon="el-icon-close" circle size="mini"
                     @click="close()"></el-button>
        </el-tooltip>
      </div>
      <div slot="widgetsList">
        <div v-if="myCompsList.length<=0" class="widgets-list-nodata">
          <el-empty description="没有部件啦" :image-size="60"></el-empty>
        </div>
        <div class="widgetsListBox">
          <span v-for="item in myCompsList" :key="item.title">
            <el-tooltip class="item" effect="dark" :content="item.description" placement="top">
              <div class="widgetsListItem" :style="{background: $util.randomBackground()}">
                <span style="position: relative;right: 8px;float: right;top: -22px;cursor: pointer;"
                      @click="push(item)">
                  <i class="el-icon-plus"></i>
                </span>
                <i :class="item.icon"></i> &nbsp;{{ item.title }}
              </div>
            </el-tooltip>
          </span>
        </div>
      </div>
    </suspended-library>
    <div class="widgets" ref="widgets">
      <div :class="['widgets-wrapper',customizing?'widgets-wrapper-bg':'']">
        <div v-if="nowCompsList.length<=0" class="no-widgets">
          <el-empty image="img/no-widgets.svg" description="没有部件啦" :image-size="280"></el-empty>
        </div>
        <grid-layout
          ref="gridlayout"
          :layout.sync="layout"
          :col-num="colNum"
          :row-height="1"
          :is-draggable="customizing"
          :vertical-compact="false"
          :use-css-transforms="true"
          :autoSize="true"
        >
          <grid-item
            v-for="(item, index) in layout"
            :static="item.static"
            :x="item.x"
            :y="item.y"
            :w="item.w"
            :h="item.h"
            :i="item.i"
            :key="index"
            :isResizable="customizing"
            @container-resized="containerResizedEvent"
          >
            <div v-if="customizing" class="customize-overlay">
              <el-button v-if="item.config && Object.keys(item.config).length!==0" class="close" style="right: 60px;"
                         type="primary" plain icon="el-icon-setting" size="small"
                         @click="clickConfig(item,index)" circle></el-button>
              <el-button class="close" type="danger" plain icon="el-icon-close" size="small"
                         @click="remove(index)" circle></el-button>
              <label>
                <i :class="allComps[item.element].icon"></i>
                {{ allComps[item.element].title }}</label>
              <div style="color:#000;">宽{{ item.w }} x 高{{ item.h }}</div>
            </div>
            <component :class="customizing?'set-component-bg':''" :is="allComps[item.element]"
                       :config="item.config || {}" :width="item.w" :height="item.h" :pxData="pxData[item.i]"></component>
          </grid-item>
        </grid-layout>
      </div>
    </div>
    <dashboard-config ref="dashboardConfig" @saveConfig="saveConfig"></dashboard-config>
  </d2-container>
</template>

<script>
import draggable from 'vuedraggable'
import allComps from './components'
import VueGridLayout from 'vue-grid-layout'
import SuspendedLibrary from '@/views/dashboard/workbench/suspendedLibrary'
import DashboardConfig from '@/views/dashboard/workbench/config'
import initData from './init.js'

export default {
  components: {
    DashboardConfig,
    SuspendedLibrary,
    draggable,
    GridLayout: VueGridLayout.GridLayout,
    GridItem: VueGridLayout.GridItem
  },
  data () {
    return {
      customizing: false,
      allComps: allComps,
      selectLayout: [],
      defaultLayout: initData,
      layout: [],
      colNum: 48,
      minimize: false,
      pxData: {}
    }
  },
  async created () {
    this.layout = await this.$store.dispatch('d2admin/db/get', {
      dbName: 'sys',
      path: 'grid-layout',
      defaultValue: JSON.parse(JSON.stringify(this.defaultLayout)),
      user: true
    }, { root: true })
  },
  mounted () {
    this.$emit('on-mounted')
  },
  computed: {
    allCompsList () {
      var allCompsList = []
      for (var key in this.allComps) {
        allCompsList.push({
          key: key,
          sort: allComps[key].sort,
          title: allComps[key].title,
          icon: allComps[key].icon,
          height: allComps[key].height,
          width: allComps[key].width,
          config: allComps[key].config || {},
          isResizable: allComps[key].isResizable || null,
          description: allComps[key].description
        })
      }
      allCompsList.sort(function (a, b) {
        return (a.sort || 0) - (b.sort || 0)
      })
      return allCompsList
    },
    myCompsList () {
      return this.allCompsList
    },
    nowCompsList () {
      return this.allCompsList
    }
  },
  methods: {
    // 开启自定义
    custom () {
      this.customizing = true
      this.$refs.suspendedLibrary.menu = true
      const oldWidth = this.$refs.widgets.offsetWidth
      this.$nextTick(() => {
        const scale = this.$refs.widgets.offsetWidth / oldWidth
        this.$refs.widgets.style.setProperty('transform', `scale(${scale})`)
      })
    },
    getLayoutElementNumber (elementName) {
      return elementName + this.layout.length
    },
    // 追加
    push (item) {
      this.layout.push({
        i: this.getLayoutElementNumber(item.key),
        x: (this.layout.length * 2) % (this.colNum || 12),
        y: this.layout.length + (this.colNum || 12),
        w: item.width,
        h: item.height,
        config: item.config || {},
        isResizable: item.isResizable || null,
        element: item.key
      })
    },
    // 删除组件
    remove (index) {
      this.layout.splice(index, 1)
    },
    // 保存
    async save () {
      console.log(this.layout)
      this.customizing = false
      this.minimize = false
      this.$refs.suspendedLibrary.menu = false
      this.$refs.widgets.style.removeProperty('transform')
      var layout = JSON.parse(JSON.stringify(this.layout))
      layout.map(val => {
        delete val.pxData
      })
      await this.$store.dispatch('d2admin/db/set', {
        dbName: 'sys',
        path: 'grid-layout',
        value: layout,
        user: true
      }, { root: true })
    },
    // 恢复默认
    backDefault () {
      this.customizing = false
      this.minimize = false
      this.$refs.suspendedLibrary.menu = false
      this.$refs.widgets.style.removeProperty('transform')
      this.layout = JSON.parse(JSON.stringify(this.defaultLayout))
      // 设为默认
      this.$store.dispatch('d2admin/db/set', {
        dbName: 'sys',
        path: 'grid-layout',
        value: this.layout,
        user: true
      }, { root: true })
    },
    // 关闭
    async close () {
      this.customizing = false
      this.minimize = false
      this.$refs.suspendedLibrary.menu = false
      this.$refs.widgets.style.removeProperty('transform')
      this.layout = await this.$store.dispatch('d2admin/db/get', {
        dbName: 'sys',
        path: 'grid-layout',
        defaultValue: JSON.stringify(this.defaultLayout),
        user: true
      }, { root: true })
    },
    // 清空画布
    clickEmpty () {
      this.layout = []
    },
    // 保存配置
    saveConfig (myComp, items) {
      this.layout.map(val => {
        if (val.i === items.i) {
          val.config = JSON.parse(JSON.stringify(items.config))
        }
      })
    },
    // 最小化
    clickMinimize () {
      this.minimize = !this.minimize
      this.$refs.suspendedLibrary.menu = !this.$refs.suspendedLibrary.menu
    },
    // 打开系统配置
    clickConfig (itme) {
      this.$refs.dashboardConfig.deviceUpgradeDrawer = true
      this.$refs.dashboardConfig.initData(this.allComps[itme.element], JSON.parse(JSON.stringify(itme)))
      this.minimize = false
    },
    // 设置实际的宽度和高度
    containerResizedEvent: function (i, newH, newW, newHPx, newWPx) {
      this.layout.map(val => {
        if (val.i === i) {
          this.$set(this.pxData, val.i, {
            hpx: Number(newHPx),
            wpx: Number(newWPx)
          })
        }
      })
    }
  }
}
</script>
<style scoped lang="scss">
::v-deep .d2-container-full__body {
  padding: 0!important;
}

.widgetsListItem {
  width: 168px;
  height: 75px;
  border-radius: 4px 4px 4px 4px;
  font-size: 16px;
  font-family: Microsoft YaHei-Bold, Microsoft YaHei;
  font-weight: bold;
  color: #ffffff;
  text-align: center;
  margin-left: 7px;
  line-height: 75px;
  margin-bottom: 10px;
  position: initial;
}

.widgetsListBox {
  display: flex;
  flex-wrap: wrap;
  margin-top: 20px;
  z-index: 999999;
}

.component-header {
  background-color: #FFFFFF;
  position: sticky;
  top: -20px;
  z-index: 99;

  .set-btn-class {
    float: right;
    z-index: 99;
  }

  .all-component-class {
    clear: right;

    .widgets-list {
      display: flex;
      justify-content: space-between;
      overflow-x: scroll;
      padding-bottom: 10px;

      .widgets-list-item {
        margin-right: 10px;
      }

      .widgets-list-item:last-child {
        margin-right: 0px;
      }
    }
  }
}

.widgets-wrapper-bg {
  background: rgba(180, 180, 180, .2);
  min-height: 500px;
}

.widgets-wrapper .sortable-ghost {
  opacity: 0.5;
}

.set-component-bg {
  //background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(0, 0, 0, .5);
}

.customize-overlay {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 5px;
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

</style>
