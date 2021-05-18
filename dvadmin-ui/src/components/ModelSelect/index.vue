<!-- 通用选择器 -->
<template>
  <div>
    <treeselect v-model="select_value" :options="selectOptions" :multiple="multiple" :show-count="true"
                :placeholder="placeholder" :disable-branch-nodes="disable_branch_nodes"/>
  </div>
</template>

<script>
  import Treeselect from '@riophae/vue-treeselect'
  import "@riophae/vue-treeselect/dist/vue-treeselect.css";

  export default {
    name: "ModelSelect",
    props: {
      /* 选择器的内容 */
      value: {type: Number | Array,},
      /* 用于显示选项 */
      placeholder: {type: String, default: "请选择",},
      /* 是否多选 */
      multiple: {type: Boolean, default: false,},
      /* 是否只能选末级 */
      disable_branch_nodes: {type: Boolean, default: false,},
      /* 用于下拉显示名称的字段 */
      label_name: {type: String, default: 'name',},
      /* 选择器信息 api 对象 */
      listApi: {type: Function, default: null},
    },
    components: {Treeselect},
    data() {
      return {
        selectOptions: [],
        select_value: ''
      }
    },
    watch: {
      select_value(newValue) {
        this.$emit('update:value', newValue)
      },
      value: {
        handler: function (newValue) {
          this.select_value = newValue
        },
        immediate: true
      }
    },
    created() {
      this.getData()
    },
    methods: {
      /** 查询所有选择器信息 **/
      getData() {
        this.listApi({pageNum: "all", _fields: "id," + this.label_name}).then(response => {
          response.data.map(val => {
            val["label"] = val[this.label_name]
          })
          this.selectOptions = this.handleTree(response.data, 'id', 'parentId')
        })
      },
    }

  }
</script>

<style scoped>

</style>
