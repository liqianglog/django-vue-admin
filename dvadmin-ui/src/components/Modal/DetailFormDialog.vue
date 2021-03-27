<template>
  <el-dialog :title="dialogTitle"
             :visible="openDetailModal"
             :width="modalWidth"
             @close="closeDetailFormDialog"
             append-to-body
  >
    <el-form ref="form"
             :model="formData"
             :label-width="labelWidth"
             :size="formSize"

    >
      <el-row>
        <template v-for="item in formItem">
          <el-col :span="item.singleLine? 24:12">
            <el-form-item :label="`${item.label}：`" :key="item.index" >
              <template v-if="item.customRender">
                <slot :name="item.key" :item="item"></slot>
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
  import { parseTime } from '../../utils/ruoyi'

  const labelTypeToFunction = {
    time: (item, formData) => {
      return parseTime(formData[item.key])
    },
    boolean: (item, formData) => {
      return item.labelChoices[formData[item.key]]
    }
  }

  export default {
    name: 'DetailFormDialog',
    props: {
      dialogTitle: { type: String, required: true },
      openDetailModal: { type: Boolean, required: true },
      modalWidth: { type: String, default: '720px' },
      labelWidth: { type: String, default: '100px' },
      formSize: { type: String, default: 'mini' },
      formData: { type: Object, default: {} },
      formItem: { type: Array, default: [] }
    },
    methods: {
      parseFormItemContent(item) {
        let labelType = item.labelType
        if (labelType) {
          return labelTypeToFunction[labelType](item, this.formData)
        } else {
          return this.formData[item.key]
        }
      },
      closeDetailFormDialog() {
        this.$emit('closeDialog', false)
      }
    }

  }
</script>

<style scoped>

</style>
