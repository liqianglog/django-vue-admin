<!-- 通用选择器 -->
<template>
  <treeselect
    v-model="select_value"
    :options="selectOptions"
    :multiple="multiple"
    :show-count="true"
    :placeholder="placeholder"
    :disable-branch-nodes="disable_branch_nodes"
    style="line-height:20px"
  />
</template>

<script>
import Treeselect from "@riophae/vue-treeselect";
import "@riophae/vue-treeselect/dist/vue-treeselect.css";

export default {
  name: "ModelSelect",
  components: { Treeselect },
  props: {
    /* 选择器的内容 */
    value: { type: Number || Array },
    prop: { type: String },
    /* 用于显示选项 */
    placeholder: { type: String, default: "请选择" },
    /* 是否多选 */
    multiple: { type: Boolean, default: false },
    /* 是否只能选末级 */
    disable_branch_nodes: { type: Boolean, default: false },
    /* 用于下拉显示名称的字段 */
    label_name: { type: String, default: "name" },
    /* 选择器信息 api 对象 */
    listApi: { type: Function, default: null },
    /* 选择器信息 selectOptions 对象 */
    select_options: { type: Array, default: null }
  },
  data() {
    return {
      selectOptions: [],
      select_value: ""
    };
  },
  watch: {
    select_value(newValue) {
      this.$emit("update:value", newValue);
    },
    value: {
      handler: function(newValue) {
        this.select_value = newValue;
      },
      immediate: true
    },
    select_options: {
      handler: function(newValue) {
        if (newValue) {
          this.selectOptions = this.handleTree(newValue, "id", "parentId");
        }
      },
      immediate: true
    }
  },
  created() {
    this.getData();
  },
  methods: {
    /** 查询所有选择器信息 **/
    getData() {
      if (this.select_options) return;
      this.getModelSelect(this.prop, this.label_name, this.listApi).then(response => {
        this.selectOptions = response;
      });
    }
  }

};
</script>

<style>

</style>
