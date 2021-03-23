<!--
@description: 已封装组件、通用组件、基础组件、全局组件(已注册全局组件)
-->
<template>
  <el-dialog
    ref="elDialog"
    :visible.sync="visible"
    :loading="loading"
    :append-to-body="appendToBody"
    :width="width"
    :show-close="false"
    :destroy-on-close="destroyOnClose"
    :close-on-click-modal="closeOnClickModal"
    class="small-dialog"
    @open="open"
    @opened="opened"
    @close="close"
    @closed="closed"
  >
    <el-row slot="title">
      <el-col :span="18" style="text-align: left;">
        <common-icon :icon-title="dialogTitle || 'Dialog组件'" :value="icon" style="font-size: 1.2em"/>
      </el-col>
      <el-col :span="6" style="text-align: right">
        <i class="el-icon-close" style="font-size: 30px; cursor: pointer" title="关闭" @click="dialogClose"/>
      </el-col>
    </el-row>
    <div class="dialog-body">
      <slot/>
    </div>
    <slot name="footer">
      <div class="dialog-button">
        <el-button v-if="buttons.indexOf('cancel') >= 0" :size="size" :disabled="loading" type="info" title="取消" @click="cancel">取消</el-button>
        <el-button v-if="buttons.indexOf('confirm') >= 0" :size="size" :disabled="loading" type="success" title="确定" @click="confirm">确定</el-button>
      </div>
    </slot>
  </el-dialog>

</template>
<script>
  export default {
    name: 'SmallDialog',
    props: {
      value: { type: Boolean, default: false },
      dialogTitle: { type: String, default: '' },
      width: { type: String, default: '50%' },
      icon: { type: String, default: 'el:el-icon-platform-eleme' },
      buttons: { type: Array, default: () => ['cancel', 'confirm'] },
      loading: { type: Boolean, default: false },
      appendToBody: { type: Boolean, default: false },
      destroyOnClose: { type: Boolean, default: false },
      closeOnClickModal: { type: Boolean, default: true }
    },
    data() {
      return {
        visible: false,
        size: null
      };
    },
    watch: {
      value(val) {
        this.visible = val;
      },
      visible(val) {
        this.$emit('input', val);
      }
    },
    created() {
    },
    methods: {
      open() {
        this.$emit('open');
      },
      opened() {
        this.$emit('opened');
      },
      close() {
        this.$emit('close');
      },
      closed() {
        this.$emit('closed');
      },
      confirm() {
        this.$emit('confirm');
      },
      cancel() {
        this.$emit('cancel');
        this.dialogClose();
      },
      dialogOpen() {
      },
      dialogClose() {
        this.visible = false;
      }
    }
  };
</script>
<style rel="stylesheet/scss" lang="scss">
  .small-dialog {
    .el-dialog__header {
      padding: 5px;
    }
    .el-dialog__body {
      padding: 5px;
    }
  }
</style>
<style rel="stylesheet/scss" lang="scss" scoped>
  .small-dialog {
    .dialog-body {
      padding-top: 5px;
    }
    .dialog-button {
      margin-top: 10px;
      text-align: right;
    }
  }
</style>

