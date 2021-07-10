<template>
  <el-dialog
    :title="dialogTitle"
    :visible="openDetailModal"
    :width="modalWidth"
    append-to-body
    @close="closeDetailFormDialog"
  >
    <el-form
      ref="form"
      :model="formData"
      :label-width="labelWidth"
      :size="formSize"
    >
      <el-row>
        <template v-for="(item,index) in formItem">
          <el-col :key="index" :span="item.singleLine? 24:12">
            <el-form-item :key="item.index" :label="`${item.label}：`">
              <template v-if="item.customRender">
                <slot :name="item.key" :item="item" />
              </template>
              <template v-else>
                {{ parseFormItemContent(item) }}
              </template>
            </el-form-item>
          </el-col>
        </template>
      </el-row>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="closeDetailFormDialog">关 闭</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { parseTime } from "../../utils/ruoyi";

const labelTypeToFunction = {
  time: (item, formData) => {
    return parseTime(formData[item.key]);
  },
  boolean: (item, formData) => {
    return item.labelChoices[formData[item.key]];
  }
};

export default {
  name: "DetailFormDialog",
  props: {
    dialogTitle: { type: String, required: true },
    openDetailModal: { type: Boolean, required: true },
    modalWidth: { type: String, default: "720px" },
    labelWidth: { type: String, default: "100px" },
    formSize: { type: String, default: "mini" },
    formData: { type: Object, default: {}},
    formItem: { type: Array, default: [] }
  },
  methods: {
    parseFormItemContent(item) {
      const labelType = item.labelType;
      if (labelType) {
        return labelTypeToFunction[labelType](item, this.formData);
      } else {
        return this.formData[item.key];
      }
    },
    closeDetailFormDialog() {
      this.$emit("closeDialog", false);
    }
  }

};
</script>

<style scoped>

</style>
