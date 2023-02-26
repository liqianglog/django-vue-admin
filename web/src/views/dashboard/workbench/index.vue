<template>
  <d2-container>
    <div class="component-header">
      <div class="set-btn-class">
        <el-button v-if="customizing" type="primary" icon="el-icon-check" round @click="save">完成</el-button>
        <el-button v-else type="primary" icon="el-icon-edit" round @click="custom">自定义</el-button>
      </div>
      <div v-if="customizing" class="all-component-class">
        <el-card style="margin-bottom: 20px">
          <div slot="header">
            <i class="el-icon-circle-plus"></i>
            <span>添加部件</span>
            <el-button-group style="float: right">
              <el-button type="primary" size="mini" @click="backDefaul()">恢复默认</el-button>
              <el-button type="danger" size="mini" @click="close()">关闭</el-button>
            </el-button-group>
          </div>
          <div class="widgets-list">
            <div v-if="myCompsList.length<=0" class="widgets-list-nodata">
              <el-empty description="没有部件啦" :image-size="60"></el-empty>
            </div>
            <div v-for="item in myCompsList" :key="item.title" class="widgets-list-item" @drag="onDrag($event,item)"
                 @dragend="onDragend($event,item)" draggable="true"
                 unselectable="on">
              <el-card style="width: 300px">
                <div slot="header">
                  <i :class="item.icon"></i>
                  <span> {{ item.title }}</span>
                  <el-button type="primary" style="float: right;" size="mini" @click="push(item)">添加</el-button>
                </div>
                <div class="item-info">
                  <p>{{ item.description }}</p>
                </div>
              </el-card>
            </div>
          </div>
        </el-card>
      </div>
    </div>
    <div class="widgets" ref="widgets">
      <div :class="['widgets-wrapper',customizing?'widgets-wrapper-bg':'']">
        <div v-if="nowCompsList.length<=0" class="no-widgets">
          <el-empty image="img/no-widgets.svg" description="没有部件啦" :image-size="280"></el-empty>
        </div>
        <grid-layout
          ref="gridlayout"
          :layout.sync="layout"
          :col-num="24"
          :row-height="1"
          :is-draggable="customizing"
          :vertical-compact="false"
          :use-css-transforms="true"
          :autoSize="true"
        >
          <grid-item v-for="(item, index) in layout"
                     :static="item.static"
                     :x="item.x"
                     :y="item.y"
                     :w="item.w"
                     :h="item.h"
                     :i="item.i"
                     :key="index"
                     :isResizable="customizing"

          >
            <div  v-if="customizing" class="customize-overlay">
              <el-button class="close" type="danger" plain icon="el-icon-close" size="small"
                         @click="remove(index)"></el-button>
              <label>
                <i :class="allComps[item.element].icon"></i>
                {{ allComps[item.element].title }}</label>
            </div>
            <component :class="customizing?'set-component-bg':''"  :is="allComps[item.element]"></component>
          </grid-item>
        </grid-layout>
      </div>
    </div>
  </d2-container>
</template>

<script>
import draggable from 'vuedraggable'
import allComps from './components'
import util from '@/libs/util'
import VueGridLayout from 'vue-grid-layout'
import XEUtils from 'xe-utils'
const mouseXY = { x: null, y: null }
const DragPos = { x: 0, y: 0, w: 1, h: 1, i: null }
export default {
  components: {
    draggable,
    GridLayout: VueGridLayout.GridLayout,
    GridItem: VueGridLayout.GridItem
  },
  data () {
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
  created () {
    this.layout = JSON.parse(util.cookies.get('grid-layout') || JSON.stringify(this.defaultLayout))
  },
  mounted () {
    document.addEventListener('dragover', function (e) {
      mouseXY.x = e.clientX
      mouseXY.y = e.clientY
    }, false)
    this.$emit('on-mounted')
  },
  computed: {
    allCompsList () {
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
      const oldWidth = this.$refs.widgets.offsetWidth
      this.$nextTick(() => {
        const scale = this.$refs.widgets.offsetWidth / oldWidth
        this.$refs.widgets.style.setProperty('transform', `scale(${scale})`)
      })
    },
    // 设置布局
    setLayout (layout) {
      // 暂定
    },
    getLayoutElementNumber (elementName) {
      // var index = 0
      // this.layout.map(res => {
      //   if (elementName === res.element) {
      //     index += 1
      //   }
      // })
      // return index + 1
      return elementName + this.layout.length
    },
    // 追加
    push (item) {
      console.log(1, item)
      this.layout.push({
        x: 6,
        y: 0,
        w: item.width,
        h: item.height,
        isResizable: item.isResizable || null,
        i: this.getLayoutElementNumber(item.key),
        element: item.key
      })
    },
    // 删除组件
    remove (index) {
      this.layout.splice(index, 1)
    },
    // 保存
    save () {
      console.log(this.layout)
      this.customizing = false
      this.$refs.widgets.style.removeProperty('transform')
      util.cookies.set('grid-layout', this.layout)
    },
    // 恢复默认
    backDefaul () {
      this.customizing = false
      this.$refs.widgets.style.removeProperty('transform')
      this.layout = JSON.parse(JSON.stringify(this.defaultLayout))
      util.cookies.remove('grid-layout')
    },
    // 关闭
    close () {
      this.customizing = false
      this.$refs.widgets.style.removeProperty('transform')
    },
    // 拖拽事件
    onDrag (e, item) {
      const { key, width, height } = item
      const parentRect = this.$refs.widgets.getBoundingClientRect()
      let mouseInGrid = false
      if (((mouseXY.x > parentRect.left) && (mouseXY.x < parentRect.right)) && ((mouseXY.y > parentRect.top) && (mouseXY.y < parentRect.bottom))) {
        mouseInGrid = true
      }
      const cloneLayout = XEUtils.clone(this.layout, true)
      if (mouseInGrid === true && (cloneLayout.findIndex(item => item.i === this.getLayoutElementNumber(key)) === -1)) {
        // this.layout.push({
        //   x: (this.layout.length * 2) % (this.colNum || 12),
        //   y: this.layout.length + (this.colNum || 12), // puts it at the bottom
        //   w: width,
        //   h: height,
        //   i: this.getLayoutElementNumber(key),
        //   element: key
        // })
      }
      const index = this.layout.findIndex(item => item.i === this.getLayoutElementNumber(key))
      if (index !== -1) {
        try {
          this.$refs.gridlayout.$children[this.layout.length].$refs.item.style.display = 'none'
        } catch {
        }
        const el = this.$refs.gridlayout.$children[index]
        el.dragging = { top: mouseXY.y - parentRect.top, left: mouseXY.x - parentRect.left }
        const new_pos = el.calcXY(mouseXY.y - parentRect.top, mouseXY.x - parentRect.left)
        if (mouseInGrid === true) {
          this.$refs.gridlayout.dragEvent('dragstart', this.getLayoutElementNumber(key), new_pos.x, new_pos.y, 1, 1)
          DragPos.i = String(index)
          DragPos.x = this.layout[index].x
          DragPos.y = this.layout[index].y
        }
        if (mouseInGrid === false) {
          this.$refs.gridlayout.dragEvent('dragend', this.getLayoutElementNumber(key), new_pos.x, new_pos.y, 1, 1)
          this.layout = this.layout.filter(obj => obj.i !== this.getLayoutElementNumber(key))
        }
      }
    },
    onDragend (e, item) {
      const { key, width, height } = item
      const parentRect = this.$refs.widgets.getBoundingClientRect()
      let mouseInGrid = false
      if (((mouseXY.x > parentRect.left) && (mouseXY.x < parentRect.right)) && ((mouseXY.y > parentRect.top) && (mouseXY.y < parentRect.bottom))) {
        mouseInGrid = true
      }
      if (mouseInGrid === true) {
        this.layout.push({
          x: DragPos.x,
          y: DragPos.y,
          w: width,
          h: height,
          i: this.getLayoutElementNumber(key),
          element: key
        })
        this.$refs.gridlayout.dragEvent('dragend', this.getLayoutElementNumber(key), DragPos.x, DragPos.y, 1, 1)
        this.layout = this.layout.filter(obj => obj.i !== this.getLayoutElementNumber(key))
        // UNCOMMENT below if you want to add a grid-item
        /*
        this.layout.push({
            x: DragPos.x,
            y: DragPos.y,
            w: 1,
            h: 1,
            i: DragPos.i,
        });
        this.$refs.gridLayout.dragEvent('dragend', DragPos.i, DragPos.x,DragPos.y,1,1);
        try {
            this.$refs.gridLayout.$children[this.layout.length].$refs.item.style.display="block";
        } catch {
        }
        */
      }
    }
  }
}
</script>
<style scoped lang="scss">
.component-header {
  background-color: #FFFFFF;
  position: sticky;
  top: -20px;
  z-index: 99;

  .set-btn-class {
    float: right;
    z-index: 99;
    margin-bottom: 10px;
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

.set-component-bg{
  background:rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(0,0,0,.5);
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

.customize-overlay .close:focus, .customize-overlay .close:hover {
  background: #76B1F9;
}

</style>
