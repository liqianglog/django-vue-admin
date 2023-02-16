<template>
  <el-select popper-class="popperClass" class="tableSelector" :multiple="props.tableConfig.isMultiple" @remove-tag="removeTag" v-model="data" placeholder="Select">
    <template #empty>
      <div class="option">
        <el-input style="margin-bottom: 10px" v-model="search">
          <template #append>
            搜索
          </template>
        </el-input>
        <el-table
            :data="props.tableConfig.data"
            size="mini"
            border
            style="width: 400px"
            max-height="200"
            :highlight-current-row="!props.tableConfig.isMultiple"
            @selection-change="handleSelectionChange"
            @current-change="handleCurrentChange"
        >
          <el-table-column v-if="props.tableConfig.isMultiple" fixed type="selection" width="55"/>
          <el-table-column fixed type="index" label="#" width="50" />
          <el-table-column prop="date" label="Date" width="180"/>
          <el-table-column prop="name" label="Name" width="180"/>
          <el-table-column prop="address" label="Address" width="300"/>
          <el-table-column prop="address" label="Address" width="300"/>
          <el-table-column prop="address" label="Address" width="300"/>
          <el-table-column prop="address" label="Address" width="300"/>
        </el-table>
        <el-pagination style="margin-top: 10px" background layout="prev, pager, next" :total="1000"/>
      </div>
    </template>
  </el-select>
</template>

<script setup lang="ts">
import {defineProps, onMounted, ref, watch} from 'vue'

const props = defineProps({
  modelValue: {},
  label: null,
  value:null,
  tableConfig: {
    data: [],//默认数据
    isMultiple: false, //是否多选
  }
} as any)
const emit = defineEmits(['update:modelValue'])
// template上使用data
const data = ref()
const multipleSelection = ref()
watch(multipleSelection, // 监听multipleSelection的变化，
    (value) => {
      const {tableConfig,label} = props
      if(!tableConfig.isMultiple){
       data.value = value?value[label]:null
      }else{

        const result = value?value.map((item:any)=>{
          return item[props.label]
        }):null
        data.value = result
      }
    }, // 当multipleSelection值触发后，同步修改data.value的值
    {immediate: true} // 立即触发一次，给data赋值初始值
)

const removeTag = (val:any,aa:any)=>{
  console.log(val,aa)
}

/**
 * 表格多选
 * @param val:Array
 */
const handleSelectionChange = (val:any) => {
  multipleSelection.value = val
  const {value} = props
  const result = val.map((item:any)=>{
    return item[value]
  })
  emit('update:modelValue', result)
}

/**
 * 表格单选
 * @param val:Object
 */
const handleCurrentChange = (val:any) => {
  multipleSelection.value = val
  const {value} = props
  emit('update:modelValue', val[value])
}

</script>

<style scoped>
.option {
  height: auto;
  line-height: 1;
  padding: 5px;
  background-color: #fff;
}

</style>
<style lang="scss">
.popperClass {
  height: 320px;
}
.el-select-dropdown__wrap {
  max-height: 310px !important;
}
.tableSelector{
.el-icon,.el-tag__close{
  display: none;
}
}
</style>
