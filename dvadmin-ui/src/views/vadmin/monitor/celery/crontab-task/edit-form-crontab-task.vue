<!--
@author: xuchi
@description: 接口编辑组件
-->
<template>
  <small-dialog
    ref="dialog"
    v-model="dialogVisible"
    :dialog-title="dialogTitle"
    :width="width"
    icon="svg:icon-interface"
    @confirm="handleSubmit"
    @closed="dialogClose"
    @opened="dialogOpen">
    <el-form v-loading="loading" ref="form" :model="form" :size="$ELEMENT.size" label-width="120px">
      <el-form-item v-show="false" prop="instanceId" label="instanceId" style="width: 200px;">
        <el-input v-model="form.instanceId" readonly/>
      </el-form-item>
      <el-form-item prop="minute" label="分钟:">
        <el-input v-model="form.minute" placeholder="默认: * "/>
      </el-form-item>
      <el-form-item prop="hour" label="小时:">
        <el-input v-model="form.hour" placeholder="默认: * "/>
      </el-form-item>
      <el-form-item prop="day_of_week" label="每周的周几">
        <el-input v-model="form.day_of_week" placeholder="默认: * "/>
      </el-form-item>
      <el-form-item prop="day_of_month" label="每月的某天">
        <el-input v-model="form.day_of_month" placeholder="默认: * "/>
      </el-form-item>
      <el-form-item prop="month_of_year" label="每年的某月">
        <el-input v-model="form.month_of_year" placeholder="默认: * "/>
      </el-form-item>
    </el-form>
  </small-dialog>
</template>
<script>
  import * as SyncDataApi from "@/api/vadmin/monitor/celery";
  export default {
    props: {
      entity: { type: Object, default: null },
      value: { type: Boolean, default: null },
      create: { type: Boolean, default: false },
      width: { type: String, default: '50%' },
      tags: { type: Array, default: () => [] }
    },
    data() {
      return {
        loading: false,
        dialogVisible: false,
        form: {
          instanceId: '',
          minute: '*',
          hour: '*',
          day_of_week: '*',
          day_of_month: '*',
          month_of_year: '*'
        }
      };
    },
    computed: {
      dialogTitle() {
        return this.create ? '新增任务定时' : '编辑任务定时';
      }
    },
    watch: {
      value(val) {
        this.dialogVisible = val;
      },
      dialogVisible(val) {
        this.$emit('input', val);
      }
    },
    created() {
    },
    methods: {
      dialogOpen() {
        // 为True意味着是通过遍及方式打开对话框
        if (!this.create) {
          this.form = { ...this.entity };
        }
      },
      handleSubmit() {
        this.$refs['form'].validate((valid) => {
          if (valid) {
            this.loading = true;
            const data = { ...this.form };
            console.log(this.form);
            if (this.create) {
              delete data['instanceId'];
              SyncDataApi.createCrontabSchedule(data).then(response => {
                this.loading = false;
                this.$emit('success', response.data);
                this.dialogClose();
                this.msgSuccess('新增成功!');
              }).catch(() => {
                this.loading = false;
              });
            } else {
              SyncDataApi.updateCrontabSchedule(data).then(response => {
                this.$emit('success', response.data);
                this.loading = false;
                this.msgSuccess('更新成功!');
                this.dialogClose();
              }).catch(() => {
                this.loading = false;
              });
            }
          } else {
            return false;
          }
        });
      },
      dialogClose() {
        this.$refs['form'].resetFields();
        this.$parent.initData();
        this.dialogVisible = false;
      }
    }
  };
</script>

