<!-- 用户选择器 -->
<template>
  <div>
    <treeselect v-model="users_value" :options="usersOptions" :multiple="multiple" :show-count="true"
                :placeholder="placeholder" :disable-branch-nodes="disable_branch_nodes"/>
  </div>
</template>

<script>
  import Treeselect from '@riophae/vue-treeselect'
  import "@riophae/vue-treeselect/dist/vue-treeselect.css";
  import {listUser} from '@/api/vadmin/permission/user'

  export default {
    name: "DeptTree",
    props: {
      /* 选择器的内容 */
      value: {type: Number | Array,},
      /* 用于显示选项 */
      placeholder: {type: String, default: "请选择用户",},
      /* 是否多选 */
      multiple: {type: Boolean, default: false,},
      /* 是否只能选末级 */
      disable_branch_nodes: {type: Boolean, default: false,},
    },
    components: {Treeselect},
    data() {
      return {
        usersOptions: [],
        users_value: ''
      }
    },
    watch: {
      users_value(newValue) {
        this.$emit('update:value', newValue)
      },
      value: {
        handler: function(newValue) {
          this.users_value = newValue
        },
        immediate: true
      }
    },
    created() {
      this.getTreeselect()
    },
    methods: {
      /** 查询所有用户信息 **/
      getTreeselect() {
        listUser({pageNum: "all", _fields: "id,name"}).then(response => {
          response.data.map(val => { val["label"] = val['name'] })
          this.usersOptions = this.handleTree(response.data, 'id')
        })
      },
    }

  }
</script>

<style scoped>

</style>
