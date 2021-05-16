<template>
  <div>
    <model-display :listApi="listApi" :fields="fields" :funcs="funcs"></model-display>
  </div>
</template>

<script>
  import * as Project from '../../../api/project/project';

  export default {
    name: "project",
    data() {
      return {
        listApi: Project.listProject,
        fields: [
          {prop: 'id', label: 'ID', show: false, unique: true, required: false},
          {prop: 'name', label: '项目名称', show: true, search: true, form: true, required: true,},
          {prop: 'code', label: '项目编码', show: true, search: true, form: true, required: true,},
          {prop: 'person', label: '项目负责人', show: true, search: true, sortable: true, type: 'users', form:true,required: true,},
          {prop: 'dept', label: '部门', show: true, search: true, type: 'depts', form:true,required: true},
          {prop: 'create_datetime', label: '创建时间', show: true, search: true, type: 'date'},
          {prop: 'creator_name', label: '创建者', show: true, search: false},
          {prop: 'description', label: '描述', show: true, search: false, form:true}
        ],
        funcs: [
          {type: 'add', label: '新增', permis: ['project:project:post'], 'icon': 'el-icon-plus', api:Project.addProject},
          {type: 'update', label: '修改', permis: ['project:project:{id}:put'], api: Project.updateProject},
          {type: 'delete', label: '删除', permis: ['project:project:{id}:delete'], api: Project.delProject},
          {type: 'export', label: '导出', permis: ['project:project:export:get'], api: Project.exportProject},
          {type: 'import', label: '导入', permis: ['project:project:importTemplate:get','project:project:importTemplate:post'], api: Project.importsProject, template_api:Project.importTemplate},
          {type: 'select', label: '详情', permis: ['project:project:get'], api: Project.getProject},
        ],
      }
    },
    created() {
    },
    mounted() {
    },
    methods: {
    }

  }
</script>
