<!--
@author: ruoxing
@description: 封装组件, 适配django ORM的高级搜索组件
-->
<template>
  <div>
    <el-row>
      <el-col v-for="(field, index) in fields" :key="index" :span="12" style="margin-bottom: 5px">
        <div v-if="field['type'] === 'date' && isDateRange(field)">
          <el-select v-model="advancedSearchValue[field['prop']]" :size="$ELEMENT.size" placeholder="请选择" class="customer-lookup-select">
            <el-option v-for="(lookup, prop, index2) in getFieldLookups(field['type'])" :key="index2" :value="prop" :label="lookup"/>
          </el-select>
          <el-date-picker
            v-model="value[field['prop']]"
            :placeholder="field['label']"
            :size="$ELEMENT.size"
            type="date"
            class="picker customer-input"
            value-format="yyyy-MM-dd"
          />
        </div>
        <div v-else-if="field['type'] === 'date' && isDateRange(field)">
          <el-select v-model="advancedSearchValue[field['prop']]" :size="$ELEMENT.size" placeholder="请选择" class="customer-lookup-select">
            <el-option v-for="(lookup, prop, index2) in getFieldLookups(field['type'])" :key="index2" :value="prop" :label="lookup"/>
          </el-select>
          <el-date-picker
            v-model="value[field['prop']]"
            :placeholder="field['label']"
            :size="$ELEMENT.size"
            type="daterange"
            align="right"
            class="customer-input"
            unlink-panels
            range-separator="-"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="yyyy-MM-dd"
          />
        </div>
        <div v-else-if="field['type'] === 'time' && isDateRange(field)">
          <el-select v-model="advancedSearchValue[field['prop']]" :size="$ELEMENT.size" placeholder="请选择" class="customer-lookup-select">
            <el-option v-for="(lookup, prop, index2) in getFieldLookups(field['type'])" :key="index2" :value="prop" :label="lookup"/>
          </el-select>
          <el-time-picker
            v-model="value[field['prop']]"
            :placeholder="field['label']"
            :size="$ELEMENT.size"
            type="time"
            class="picker customer-input"
          />
        </div>
        <div v-else-if="field['type'] === 'time' && isDateRange(field)">
          <el-select v-model="advancedSearchValue[field['prop']]" :size="$ELEMENT.size" placeholder="请选择" class="customer-lookup-select">
            <el-option v-for="(lookup, prop, index2) in getFieldLookups(field['type'])" :key="index2" :value="prop" :label="lookup"/>
          </el-select>
          <el-time-picker
            v-model="value[field['prop']]"
            :placeholder="field['label']"
            :size="$ELEMENT.size"
            is-range
            range-separator="-"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            class="customer-input"
          />
        </div>
        <div v-else-if="field['type'] === 'datetime' && !isDateRange(field)">
          <el-select v-model="advancedSearchValue[field['prop']]" :size="$ELEMENT.size" placeholder="请选择" class="customer-lookup-select">
            <el-option v-for="(lookup, prop, index2) in getFieldLookups(field['type'])" :key="index2" :value="prop" :label="lookup"/>
          </el-select>
          <el-date-picker
            v-model="value[field['prop']]"
            :placeholder="field['label']"
            :size="$ELEMENT.size"
            class="picker customer-input"
            type="datetime"
            value-format="yyyy-MM-dd HH:mm:SS"
          />
        </div>
        <div v-else-if="field['type'] === 'datetime' && isDateRange(field)">
          <el-select v-model="advancedSearchValue[field['prop']]" :size="$ELEMENT.size" placeholder="请选择" class="customer-lookup-select">
            <el-option v-for="(lookup, prop, index2) in getFieldLookups(field['type'])" :key="index2" :value="prop" :label="lookup"/>
          </el-select>
          <el-date-picker
            v-model="value[field['prop']]"
            :placeholder="field['label']"
            :size="$ELEMENT.size"
            :start-placeholder="field['label'] + '的开始'"
            :end-placeholder="field['label'] + '的结束'"
            type="datetimerange"
            class="customer-input"
            is-range
            arrow-control
            range-separator="-"
            value-format="yyyy-MM-dd HH:mm:SS"
          />
        </div>

        <div v-else-if="field['type'] === 'choices'">
          <el-select v-model="advancedSearchValue[field['prop']]" :size="$ELEMENT.size" placeholder="请选择" class="customer-lookup-select">
            <el-option v-for="(lookup, prop, index2) in getFieldLookups(field['type'])" :key="index2" :value="prop" :label="lookup"/>
          </el-select>
          <el-select v-model="value[field['prop']]" :size="$ELEMENT.size" :placeholder="field['label']" class="customer-value-select" multiple>
            <el-option
              v-for="item in field['choices']"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </div>
        <div v-else-if="field['type'] === 'boolean'">
          <el-select v-model="advancedSearchValue[field['prop']]" :size="$ELEMENT.size" placeholder="请选择" class="customer-lookup-select">
            <el-option v-for="(lookup, prop, index2) in getFieldLookups(field['type'])" :key="index2" :value="prop" :label="lookup"/>
          </el-select>
          <el-select v-model="value[field['prop']]" :size="$ELEMENT.size" :placeholder="field['label']" class="customer-value-select">
            <el-option :value="false" label="否"/>
            <el-option :value="true" label="是"/>
          </el-select>
        </div>
        <div v-else>
          <el-input
            v-model="value[field['prop']]"
            :placeholder="inputPlaceholder(field)"
            :size="$ELEMENT.size"
            style="width: 370px;"
          >
            <el-select
              slot="prepend"
              v-model="advancedSearchValue[field['prop']]"
              :size="$ELEMENT.size"
              placeholder="请选择"
              style="width: 120px">
              <el-option v-for="(lookup, prop, index2) in getFieldLookups(field['type'])" :key="index2" :value="prop" :label="lookup"/>
            </el-select>
          </el-input>
        </div>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="12">
        <el-button
          :size="$ELEMENT.size"
          name="search"
          type="primary"
          icon="el-icon-search"
          @click="handleAdvancedSearchFormSubmit">搜索
        </el-button>
        <el-button
          :size="$ELEMENT.size"
          name="refresh"
          type="warning"
          icon="el-icon-refresh"
          title="重置高级搜索表单"
          @click="handleAdvancedSearchFormReset">重置
        </el-button>
      </el-col>
    </el-row>
  </div>
</template>
<script>
  export default {
    name: 'AdvancedSearchForm',
    props: {
      value: {
        type: Object,
        default: () => {}
      },
      fields: {
        type: Array,
        default: () => []
      }
    },
    data() {
      return {
        showFields: [
        ], // 显示的字段
        showAdvancedSearchForm: false,
        advancedSearchValue: {
        },
        fieldLookups: {
          'string': {
            iexact: '精确匹配',
            in: '多值匹配',
            icontains: '模糊匹配',
            istartswith: '匹配开头',
            iendswith: '匹配结尾',
            iregex: '正则匹配'
          },
          'boolean': {
            exact: '精确匹配'
          },
          'choices': {
            exact: '精确匹配'
          },
          'int': {
            exact: '等于',
            lt: '小于',
            lte: '小于等于',
            gt: '大于',
            gte: '大于等于',
            range: '范围'
          },
          'time': {
            range: '时间范围',
            lt: '日期之前',
            gt: '日期之后',
            exact: '时间等于'
          },
          'date': {
            range: '日期范围',
            lt: '日期之前',
            gt: '日期之后',
            exact: '日期等于'
          },
          'datetime': {
            range: '日期范围',
            lt: '日期之前',
            gt: '日期之后',
            exact: '日期等于'
          }
        }
      };
    },
    computed: {
      showInput: function() {
        return function(lookup = '') {
          return ['isnull'].indexOf(lookup) < 0;
        };
      },
      isDateRange() {
        return function(field) {
          return this.advancedSearchValue[field['prop']] === 'range';
        };
      },
      inputPlaceholder: function() {
        return function(field) {
          const prop = field.prop;
          const lookup = this.advancedSearchValue[prop];
          if (lookup === 'in') {
            return `${field.label} 多个值用,或;隔开`;
          } else if (lookup === 'range') {
            return `${field.label} 两值间用,或;隔开`;
          }
          return `${field.label}`;
        };
      }
    },
    watch: {
      fields(newValue, oldValue) {
      }
    },
    mounted() {
      const advancedSearchValue = {};
      for (const searchField of this.fields) {
        const prop = searchField['prop'];
        const lookups = Object.keys(this.fieldLookups[searchField.type]);
        if (lookups.length) {
          const lookup = lookups[0];
          advancedSearchValue[prop] = lookup;
        }
      }
      // console.dir(advancedSearchValue);
      this.advancedSearchValue = advancedSearchValue;
    },
    created() {
    },
    methods: {
      getFieldLookups(type) {
        type = type || 'string';
        return this.fieldLookups[type];
      },
      getField(prop) {
        return this.fields.filter(field => field.prop === prop)[0];
      },
      getAdvancedSearchParams() {
        const params = {};
        for (const prop of Object.keys(this.value)) {
          let value = this.value[prop];
          const field = this.getField(prop);
          const lookup = this.advancedSearchValue[prop];
          if (!value) {
            continue;
          }
          let key = prop + '__' + lookup;
          if (lookup === 'in' && field.type === 'string') {
            value = value.split(/[,，;]/);
          } else if (lookup === 'range' && field.type === 'int') {
            value = value.split(/[,，;]/);
            value = value.map(ele => parseInt(ele));
          }
          if (Array.isArray(value) && field.type === 'choices') {
            if (!value.length) {
              continue;
            }
            key = prop + '__in';
          }
          params[key] = value;
        }
        // console.dir(params);
        return params;
      },
      // 处理点击高级搜索按钮事件
      handleAdvancedSearchFormSubmit() {
        const params = this.getAdvancedSearchParams();
        this.$emit('submit', params);
      },
      handleAdvancedSearchFormReset() {
        this.$emit('reset', this.value);
      }
    }
  };
</script>

<style scoped>
  .customer-lookup-select {
    width: 120px;
    margin-right: 0
  }
  .customer-value-select {
    width: 250px;
    margin-left: -3px
  }
  .el-row {
    margin-bottom: 20px;
  }
  .picker {
    width: 250px;
  }
  .customer-input {
    margin-left: -4px;
  }
</style>
