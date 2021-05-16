<!-- 部门选择器 -->
<template>
  <div>
    <treeselect v-model="dept_value" :options="deptTree" :multiple="multiple" :show-count="true"
                :placeholder="placeholder" :disable-branch-nodes="disable_branch_nodes"/>
  </div>
</template>

<script>
  import Treeselect from '@riophae/vue-treeselect'
  import "@riophae/vue-treeselect/dist/vue-treeselect.css";
  import {treeselect} from '@/api/vadmin/permission/dept'

  export default {
    name: "DeptTree",
    props: {
      /* 选择器的内容 */
      value: {type: Number | Array,},
      /* 用于显示选项 */
      placeholder: {type: String, default: "请选择归属部门",},
      /* 是否多选 */
      multiple: {type: Boolean, default: false,},
      /* 是否只能选末级 */
      disable_branch_nodes: {type: Boolean, default: false,},
    },
    components: {Treeselect},
    data() {
      return {
        deptOptions: [],
        deptTree: [],
        dept_value: ''
      }
    },
    watch: {
      dept_value(newValue) {
        this.$emit('update:value', newValue)
      },
      value: {
        handler: function (newValue) {
          this.dept_value = newValue
        },
        immediate: true
      }
    },
    created() {
      this.getTreeselect()
    },
    methods: {
      /** 查询部门下拉树结构 */
      getTreeselect() {
        treeselect().then(response => {
          this.deptOptions = response.data
          this.deptTree = this.handleTree(response.data, 'id')
        })
      },
    }

  }
</script>

<style scoped>

</style>
