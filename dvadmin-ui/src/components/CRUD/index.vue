<template>
  <div>

  </div>
</template>

<script>
  export default {
    name: "CRUD",
    data() {
      return {
        api: PermissionInterfaceApi.listPermissionInterface,
        fields: [
          // prop,后端列名称, 必填; label,前端表头名称, 必填; 其他可有可无
          { prop: 'instanceId', label: 'instanceId', show: false, unique: true },
          { prop: 'project', label: '所属项目', show: true, search: true },
          { prop: 'title', label: '标题', show: true, search: true },
          { prop: 'path', label: '路径', show: true, search: true, sortable: true },
          { prop: 'method', label: '方法', show: true, search: true, sortable: true, width: 80, type: 'choices',
            choices: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS', 'TRACE']
          },
          { prop: 'name', label: '权限名称', show: true, search: true, sortable: true },
          { prop: 'status', label: '状态', show: true, search: true, sortable: true, width: 80, type: 'choices',
            choices: [{ value: -1, label: '禁用' }, { value: 0, label: '正常' }, { value: 1, label: '开放' }]
          },
          { prop: 'tag', label: '标签', show: true, search: true, sortable: true },
          { prop: 'creator', label: '创建者', show: false, search: true },
          { prop: 'modifier', label: '更新者', show: false, search: true },
          { prop: 'mtime', label: '修改时间', show: false, search: true, type: 'datetime' },
          { prop: 'ctime', label: '创建时间', show: false, search: true, type: 'datetime' },
          { prop: 'description', label: '描述', search: true }
        ],
      }
    },
    created() {
    },
    mounted() {
    },
    methods: {}

  }
</script>

<style scoped>

</style>
