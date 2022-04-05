<template>
  <d2-container>
    <div>
      <el-header>
        <div class="yxt-flex-between">
          <div>
            <el-tag>系统配置:您可以对您的网站进行自定义配置</el-tag>
          </div>
          <div>
            <el-button-group>
              <el-button
                type="primary"
                size="small"
                icon="el-icon-folder-add"
                @click="tabsDrawer=true"
              >
                添加分组
              </el-button>
              <el-button
                size="small"
                type="warning"
                icon="el-icon-edit-outline"
                @click="contentDrawer=true"
              >
                添加内容
              </el-button>
            </el-button-group>
          </div>
        </div>
      </el-header>
    </div>
    <div>
      <el-drawer
        v-if="tabsDrawer"
        title="添加分组"
        :visible.sync="tabsDrawer"
        direction="rtl"
        size="30%"
      >
        <addTabs></addTabs>
      </el-drawer>
    </div>
    <div>
      <el-drawer
        v-if="contentDrawer"
        title="添加内容"
        :visible.sync="contentDrawer"
        direction="rtl"
        size="30%"
      >
        <addContent></addContent>
      </el-drawer>
    </div>
    <el-tabs type="border-card" v-model="editableTabsValue">
      <el-tab-pane
        :key="index"
        v-for="(item, index) in editableTabs"
        :label="item.title"
        :name="item.key"
      >
        <formContent  :options="item" :editableTabsItem="item"></formContent>
      </el-tab-pane>
    </el-tabs>
  </d2-container>
</template>

<script>
import addTabs from './components/addTabs'
import * as api from './api'
import addContent from './components/addContent'
import formContent from './components/formContent'

export default {
  name: 'config',
  components: {
    addTabs,
    addContent,
    formContent
  },
  data () {
    return {
      tabsDrawer: false,
      contentDrawer: false,
      editableTabsValue: 'basic',
      editableTabs: [],
      tabIndex: 2
    }
  },
  methods: {
    getTabs () {
      api.GetList({
        limit: 999,
        parent__isnull: true
      }).then(res => {
        const { data } = res.data
        this.editableTabs = data
      })
    }
  },
  created () {
    this.getTabs()
  }
}
</script>

<style scoped>

</style>
