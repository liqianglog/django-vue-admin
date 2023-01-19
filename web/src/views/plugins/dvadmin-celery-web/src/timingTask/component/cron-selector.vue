<!--
 * @创建文件时间: 2021-08-21 14:47:15
 * @Auther: 猿小天
 * @最后修改人: 猿小天
 * @最后修改时间: 2021-08-21 15:34:26
 * 联系Qq:1638245306
 * @文件介绍:
-->
<template>
  <div>
    <el-input
      v-popover:popover
      v-model="value"
      :disabled="disabled"
      :placeholder="placeholder"
    />
    <el-popover
      ref="popover"
      placement="bottom"
      title="corn操作"
      width="600"
      trigger="click"
    >
      <div style="text-align: left; width: 600px">
        <el-form :inline="true" size="small">
          <!-- <el-form-item style="width: 70px">
            <el-input
              ref="second"
              v-model="secondValue"
              readonly
              @focus="tabClick('second')"
            ></el-input>
          </el-form-item> -->
          <el-form-item>
            <el-input
              ref="minute"
              v-model="minuteValue"
              readonly
              @focus="tabClick('minute')"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-input
              ref="hour"
              v-model="hourValue"
              readonly
              @focus="tabClick('hour')"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-input
              ref="day"
              v-model="dayValue"
              readonly
              @focus="tabClick('day')"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-input
              ref="month"
              v-model="monthValue"
              readonly
              @focus="tabClick('month')"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-input
              ref="week"
              v-model="weekValue"
              readonly
              @focus="tabClick('week')"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-input
              ref="year"
              v-model="yearValue"
              readonly
              @focus="tabClick('year')"
            ></el-input>
          </el-form-item>
        </el-form>
        <el-tabs
          type="border-card"
          @tab-click="tabClick(tabName)"
          v-model="tabName"
        >
          <!-- <el-tab-pane label="秒" name="second">
            <el-radio-group v-model="secondRadio" @change="secondChange">
              <div class="radio-left">
                <el-radio :label="1">
                  <span class="color-red">{{ secondForm.default }}</span>
                  <span>每秒</span>
                </el-radio>
              </div>
              <div class="radio-left">
                <el-radio :label="2">
                  <span class="color-red"
                    >{{ secondForm.start }}/{{ secondForm.end }}</span
                  >
                  从第
                  <el-input-number
                    v-model="secondForm.start"
                    size="small"
                    :precision="0"
                    :min="0"
                    :max="59"
                  ></el-input-number
                  >秒 开始每
                  <el-input-number
                    v-model="secondForm.end"
                    size="small"
                    :precision="0"
                    :min="1"
                    :max="59"
                  ></el-input-number
                  >秒
                </el-radio>
              </div>
              <div class="radio-left">
                <el-radio :label="3">
                  <span class="color-red"
                    >{{ secondForm.rangeStart }}-{{ secondForm.rangeEnd }}</span
                  >
                  在
                  <el-input-number
                    v-model="secondForm.rangeStart"
                    size="small"
                    :precision="0"
                    :min="0"
                    :max="secondForm.rangeEnd"
                  ></el-input-number
                  >秒 到
                  <el-input-number
                    v-model="secondForm.rangeEnd"
                    size="small"
                    :precision="0"
                    :min="secondForm.rangeStart"
                    :max="59"
                  ></el-input-number
                  >之间的每秒
                </el-radio>
              </div>
              <div class="radio-left">
                <el-radio :label="4">
                  <span class="color-red">,</span>
                  <span>固定的</span>
                  <el-select
                    v-model="secondForm.fixed"
                    size="small"
                    multiple
                    collapse-tags
                    placeholder="请选择(支持多选)"
                  >
                    <el-option
                      v-for="(item, index) in 60"
                      :key="index"
                      :label="index"
                      :value="index"
                    ></el-option>
                  </el-select>
                </el-radio>
              </div>
            </el-radio-group>
          </el-tab-pane> -->
          <el-tab-pane label="分" name="minute">
            <el-radio-group v-model="minuteRadio" @change="minuteChange">
              <div class="radio-left">
                <el-radio :label="1">
                  <span class="color-red">{{ minuteForm.default }}</span>
                  <span>每分</span>
                </el-radio>
              </div>
              <!-- <div class="radio-left">
                <el-radio :label="2">
                  <span class="color-red"
                    >{{ minuteForm.start }}/{{ minuteForm.end }}</span
                  >
                  从第
                  <el-input-number
                    v-model="minuteForm.start"
                    size="small"
                    :precision="0"
                    :min="0"
                    :max="59"
                  ></el-input-number
                  >分 开始每
                  <el-input-number
                    v-model="minuteForm.end"
                    size="small"
                    :precision="0"
                    :min="1"
                    :max="59"
                  ></el-input-number
                  >分
                </el-radio>
              </div> -->
              <div class="radio-left">
                <el-radio :label="3">
                  <span class="color-red"
                    >{{ minuteForm.rangeStart }}-{{ minuteForm.rangeEnd }}</span
                  >
                  在
                  <el-input-number
                    v-model="minuteForm.rangeStart"
                    size="small"
                    :precision="0"
                    :min="0"
                    :max="minuteForm.rangeEnd"
                  ></el-input-number
                  >分 到
                  <el-input-number
                    v-model="minuteForm.rangeEnd"
                    size="small"
                    :precision="0"
                    :min="minuteForm.rangeStart"
                    :max="59"
                  ></el-input-number
                  >之间的每分
                </el-radio>
              </div>
              <div class="radio-left">
                <el-radio :label="4">
                  <span class="color-red">,</span>
                  <span>固定的</span>
                  <el-select
                    v-model="minuteForm.fixed"
                    size="small"
                    multiple
                    collapse-tags
                    placeholder="请选择(支持多选)"
                  >
                    <el-option
                      v-for="(item, index) in 60"
                      :key="index"
                      :label="index"
                      :value="index"
                    ></el-option>
                  </el-select>
                </el-radio>
              </div>
            </el-radio-group>
          </el-tab-pane>
          <el-tab-pane label="时" name="hour">
            <el-radio-group v-model="hourRadio" @change="hourChange">
              <div class="radio-left">
                <el-radio :label="1">
                  <span class="color-red">{{ hourForm.default }}</span>
                  <span>每时</span>
                </el-radio>
              </div>
              <!-- <div class="radio-left">
                <el-radio :label="2">
                  <span class="color-red"
                    >{{ hourForm.start }}/{{ hourForm.end }}</span
                  >
                  从第
                  <el-input-number
                    v-model="hourForm.start"
                    size="small"
                    :precision="0"
                    :min="0"
                    :max="59"
                  ></el-input-number
                  >时 开始每
                  <el-input-number
                    v-model="hourForm.end"
                    size="small"
                    :precision="0"
                    :min="1"
                    :max="59"
                  ></el-input-number
                  >时
                </el-radio>
              </div> -->
              <div class="radio-left">
                <el-radio :label="3">
                  <span class="color-red"
                    >{{ hourForm.rangeStart }}-{{ hourForm.rangeEnd }}</span
                  >
                  在
                  <el-input-number
                    v-model="hourForm.rangeStart"
                    size="small"
                    :precision="0"
                    :min="0"
                    :max="hourForm.rangeEnd"
                  ></el-input-number
                  >时 到
                  <el-input-number
                    v-model="hourForm.rangeEnd"
                    size="small"
                    :precision="0"
                    :min="hourForm.rangeStart"
                    :max="59"
                  ></el-input-number
                  >之间的每时
                </el-radio>
              </div>
              <div class="radio-left">
                <el-radio :label="4">
                  <span class="color-red">,</span>
                  <span>固定的</span>
                  <el-select
                    v-model="hourForm.fixed"
                    size="small"
                    multiple
                    collapse-tags
                    placeholder="请选择(支持多选)"
                  >
                    <el-option
                      v-for="(item, index) in 60"
                      :key="index"
                      :label="index"
                      :value="index"
                    ></el-option>
                  </el-select>
                </el-radio>
              </div>
            </el-radio-group>
          </el-tab-pane>
          <el-tab-pane label="天" name="day">
            <el-radio-group v-model="dayRadio" @change="dayChange">
              <div class="radio-left">
                <el-radio :label="1">
                  <span class="color-red">{{ dayForm.default }}</span>
                  <span>每日</span>
                </el-radio>
              </div>
              <!-- <div class="radio-left">
                <el-radio :label="2">
                  <span class="color-red"
                    >{{ dayForm.start }}/{{ dayForm.end }}</span
                  >
                  从第
                  <el-input-number
                    v-model="dayForm.start"
                    size="small"
                    :precision="0"
                    :min="1"
                    :max="59"
                  ></el-input-number
                  >日 开始每
                  <el-input-number
                    v-model="dayForm.end"
                    size="small"
                    :precision="0"
                    :min="1"
                    :max="59"
                  ></el-input-number
                  >日
                </el-radio>
              </div> -->
              <div class="radio-left">
                <el-radio :label="3">
                  <span class="color-red"
                    >{{ dayForm.rangeStart }}-{{ dayForm.rangeEnd }}</span
                  >
                  在
                  <el-input-number
                    v-model="dayForm.rangeStart"
                    size="small"
                    :precision="0"
                    :min="1"
                    :max="dayForm.rangeEnd"
                  ></el-input-number
                  >日 到
                  <el-input-number
                    v-model="dayForm.rangeEnd"
                    size="small"
                    :precision="0"
                    :min="dayForm.rangeStart"
                    :max="59"
                  ></el-input-number
                  >之间的每日
                </el-radio>
              </div>
              <div class="radio-left">
                <el-radio :label="4">
                  <span class="color-red">,</span>
                  <span>固定的</span>
                  <el-select
                    v-model="dayForm.fixed"
                    size="small"
                    multiple
                    collapse-tags
                    placeholder="请选择(支持多选)"
                  >
                    <el-option
                      v-for="(item, index) in 60"
                      :key="index+ 1"
                      :label="index + 1"
                      :value="index + 1"
                    ></el-option>
                  </el-select>
                </el-radio>
              </div>
              <div class="radio-left">
                <el-radio :label="5">
                  <span class="color-red">{{ dayForm.noFixed }}</span>
                  <span>不固定的</span>
                </el-radio>
              </div>
              <div class="radio-left">
                <el-radio :label="6">
                  <span class="color-red">L-{{ dayForm.lastDay - 1 }}</span>
                  本月倒数第
                  <el-input-number
                    v-model="dayForm.lastDay"
                    size="small"
                    :precision="0"
                    :min="1"
                    :max="31"
                  ></el-input-number
                  >日
                </el-radio>
              </div>
              <div class="radio-left">
                <el-radio :label="7">
                  <span class="color-red">{{ dayForm.workDay }}W</span>
                  每月
                  <el-input-number
                    v-model="dayForm.workDay"
                    size="small"
                    :precision="0"
                    :min="1"
                    :max="31"
                  ></el-input-number
                  >日最近的工作日
                </el-radio>
              </div>
              <div class="radio-left">
                <el-radio :label="8">
                  <span class="color-red">{{ dayForm.lastWorkDay }}</span>
                  <span>本月最后一个工作日</span>
                </el-radio>
              </div>
            </el-radio-group>
          </el-tab-pane>
          <el-tab-pane label="月" name="month">
            <el-radio-group v-model="monthRadio">
              <div class="radio-left">
                <el-radio :label="1">
                  <span class="color-red">{{ monthForm.default }}</span>
                  <span>每月</span>
                </el-radio>
              </div>
             <!--  <div class="radio-left">
                <el-radio :label="2">
                  <span class="color-red"
                    >{{ monthForm.start }}/{{ monthForm.end }}</span
                  >
                  从第
                  <el-input-number
                    v-model="monthForm.start"
                    size="small"
                    :precision="0"
                    :min="1"
                    :max="59"
                  ></el-input-number
                  >月 开始每
                  <el-input-number
                    v-model="monthForm.end"
                    size="small"
                    :precision="0"
                    :min="1"
                    :max="59"
                  ></el-input-number
                  >月
                </el-radio>
              </div> -->
              <div class="radio-left">
                <el-radio :label="3">
                  <span class="color-red"
                    >{{ monthForm.rangeStart }}-{{ monthForm.rangeEnd }}</span
                  >
                  在
                  <el-input-number
                    v-model="monthForm.rangeStart"
                    size="small"
                    :precision="0"
                    :min="1"
                    :max="monthForm.rangeEnd"
                  ></el-input-number
                  >月 到
                  <el-input-number
                    v-model="monthForm.rangeEnd"
                    size="small"
                    :precision="0"
                    :min="monthForm.rangeStart"
                    :max="59"
                  ></el-input-number
                  >之间的每月
                </el-radio>
              </div>
              <div class="radio-left">
                <el-radio :label="4">
                  <span class="color-red">,</span>
                  <span>固定的</span>
                  <el-select
                    v-model="monthForm.fixed"
                    size="small"
                    multiple
                    collapse-tags
                    placeholder="请选择(支持多选)"
                  >
                    <el-option
                      v-for="(item, index) in 60"
                      :key="index + 1"
                      :label="index + 1"
                      :value="index + 1"
                    ></el-option>
                  </el-select>
                </el-radio>
              </div>
            </el-radio-group>
          </el-tab-pane>
          <el-tab-pane label="周" name="week">
            <el-radio-group v-model="weekRadio">
              <div class="radio-left">
                <el-radio :label="1">
                  <span class="color-red">{{ weekForm.default }}</span>
                  <span>每周</span>
                </el-radio>
              </div>
              <!-- <div class="radio-left">
                <el-radio :label="2">
                  <span class="color-red"
                    >{{ weekForm.start }}/{{ weekForm.end }}</span
                  >
                  在星期
                  <el-input-number
                    v-model="weekForm.start"
                    size="small"
                    :precision="0"
                    :min="1"
                    :max="weekForm.end"
                  ></el-input-number>
                  到 星期
                  <el-input-number
                    v-model="weekForm.end"
                    size="small"
                    :precision="0"
                    :min="1"
                    :max="7"
                  ></el-input-number
                  >之间的每日
                </el-radio>
              </div> -->
              <div class="radio-left">
                <el-radio :label="3">
                  <span class="color-red"
                    >{{ weekForm.rangeStart }}-{{ weekForm.rangeEnd }}</span
                  >
                  在
                  <el-input-number
                    v-model="weekForm.rangeStart"
                    size="small"
                    :precision="0"
                    :min="1"
                    :max="weekForm.rangeEnd"
                  ></el-input-number
                  >周 到
                  <el-input-number
                    v-model="weekForm.rangeEnd"
                    size="small"
                    :precision="0"
                    :min="weekForm.rangeStart"
                    :max="59"
                  ></el-input-number
                  >之间的每周
                </el-radio>
              </div>
              <div class="radio-left">
                <el-radio :label="4">
                  <span class="color-red">,</span>
                  <span>固定的</span>
                  <el-select
                    v-model="weekForm.fixed"
                    size="small"
                    multiple
                    collapse-tags
                    placeholder="请选择(支持多选)"
                  >
                    <el-option
                      v-for="(item, index) in 60"
                      :key="index + 1"
                      :label="index + 1"
                      :value="index + 1"
                    ></el-option>
                  </el-select>
                </el-radio>
              </div>
              <div class="radio-left">
                <el-radio :label="5">
                  <span class="color-red">{{ weekForm.noFixed }}</span>
                  <span>不固定的</span>
                </el-radio>
              </div>
              <div class="radio-left">
                <el-radio :label="6">
                  <span class="color-red">{{ weekForm.lastWeek }}L</span>
                  在本月最后一个
                  <el-select
                    v-model="weekForm.lastWeek"
                    size="small"
                    placeholder="请选择"
                  >
                    <el-option
                      v-for="item in weekList"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value"
                      :disabled="item.disabled"
                    >
                    </el-option>
                  </el-select>
                </el-radio>
              </div>
              <div class="radio-left">
                <el-radio :label="7">
                  <span class="color-red"
                    >{{ weekForm.weekNum }}#{{ weekForm.monthWeek }}</span
                  >
                  本月<el-input-number
                    v-model="weekForm.monthWeek"
                    size="small"
                    :precision="0"
                    :min="1"
                    :max="5"
                  ></el-input-number
                  >个
                  <el-select
                    v-model="weekForm.weekNum"
                    size="small"
                    placeholder="请选择"
                  >
                    <el-option
                      v-for="item in weekList"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value"
                      :disabled="item.disabled"
                    >
                    </el-option>
                  </el-select>
                </el-radio>
              </div>
            </el-radio-group>
          </el-tab-pane>
          <el-tab-pane label="年" name="year">
            <el-radio-group v-model="yearRadio">
              <div class="radio-left">
                <el-radio :label="1">
                  <span class="color-red">{{ yearForm.default }}</span>
                  <span>每年</span>
                </el-radio>
              </div>
              <!-- <div class="radio-left">
                <el-radio :label="2">
                  <span class="color-red"
                    >{{ yearForm.start }}/{{ yearForm.end }}</span
                  >
                  从第
                  <el-input-number
                    v-model="yearForm.start"
                    size="small"
                    :precision="0"
                    :min="new Date().getFullYear()"
                  ></el-input-number
                  >年 开始每
                  <el-input-number
                    v-model="yearForm.end"
                    size="small"
                    :precision="0"
                    :min="1"
                  ></el-input-number
                  >年
                </el-radio>
              </div> -->
              <div class="radio-left">
                <el-radio :label="3">
                  <span class="color-red"
                    >{{ yearForm.rangeStart }}-{{ yearForm.rangeEnd }}</span
                  >
                  在
                  <el-input-number
                    v-model="yearForm.rangeStart"
                    size="small"
                    :precision="0"
                    :min="new Date().getFullYear()"
                    :max="yearForm.rangeEnd"
                  ></el-input-number
                  >年 到
                  <el-input-number
                    v-model="yearForm.rangeEnd"
                    size="small"
                    :precision="0"
                    :min="yearForm.rangeStart"
                  ></el-input-number
                  >之间的每年
                </el-radio>
              </div>
              <div class="radio-left">
                <el-radio :label="4">
                  <span class="color-red">,</span>
                  <span>固定的</span>
                  <el-select
                    v-model="yearForm.fixed"
                    size="small"
                    multiple
                    collapse-tags
                    placeholder="请选择(支持多选)"
                  >
                    <el-option
                      v-for="(item, index) in 60"
                      :key="index"
                      :label="nowYear + index"
                      :value="nowYear + index"
                    ></el-option> </el-select
                  >年
                </el-radio>
              </div>
              <div class="radio-left">
                <el-radio :label="5">
                  <span class="color-red">{{ yearForm.none }}</span>
                  <span>不配置</span>
                </el-radio>
              </div>
            </el-radio-group>
          </el-tab-pane>
          <el-tab-pane label="帮助" name="help">
            <div style="text-align: left">
              <el-form :inline="true">
                <el-form-item style="width: 56px">
                  <el-button
                    type="primary"
                    :disabled="helpForm === ''"
                    size="small"
                    @click="onHelpChange"
                    >使用</el-button
                  >
                </el-form-item>
                <el-form-item style="width: 220px">
                  <el-select
                    v-model="helpForm"
                    placeholder="请选择"
                    size="small"
                  >
                    <el-option
                      v-for="item in helpList"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value"
                    >
                      <span style="float: left">{{ item.label }}</span>
                      <span
                        style="float: right; color: #8492a6; font-size: 13px"
                        >{{ item.value }}</span
                      >
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item style="width: 220px">
                  {{ helpForm }}
                </el-form-item>
              </el-form>
              <div>
                <span>秒:值为</span><strong>0 1 2 ... 59</strong>
                <span> 通配符支持</span><strong> * - ,</strong>
              </div>
              <div>
                <span>分:值为</span><strong>0 1 2 ... 59</strong>
                <span> 通配符支持</span><strong> * - ,</strong>
              </div>
              <div>
                <span>时:值为</span><strong>0 1 2 ... 23</strong>
                <span> 通配符支持</span><strong> * - ,</strong>
              </div>
              <div>
                <span>日:值为</span><strong>0 1 2 ... 31</strong>
                <span> 通配符支持</span><strong> *  - , L W C</strong>
              </div>
              <div>
                <span>月:值为</span
                ><strong>1 2 ... 12，或12个月的缩写(JAN ... DEC) </strong>
                <span> 通配符支持</span><strong> * - ,</strong>
              </div>
              <div>
                <span>周:值为</span
                ><strong>1 2 ... 7或星期的缩写(SUN ... SAT)</strong>
                <span> 通配符支持</span><strong> * - , ? L # C</strong>
              </div>
              <div>
                <span>年:值为</span><strong>{{ nowYear }} ... 2079</strong>
                <span> 通配符支持</span><strong> * - ,</strong>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-popover>
  </div>
</template>

<script>
export default {
  name: 'cron-selector-input',
  props: {
    // 值
    value: {
      type: [Number, String, Boolean, Array, Object]
    },
    // 是否禁用
    disabled: {
      type: Boolean,
      default: false
    },
    // 提示
    placeholder: {
      type: String,
      default: '请选择'
    }
  },
  data () {
    return {
      formInline: {
        // second: '*', // 秒
        minute: '*', // 分
        hour: '*', // 小时
        day: '*', // 天
        month: '*', // 月
        week: '*', // 周
        year: '*' // 年
      },
      tabName: 'minute',
      secondRadio: 1, // 秒-选中的radio
      secondForm: {
        // 秒-form值
        default: '*',
        start: 0,
        end: 0,
        rangeStart: 0,
        rangeEnd: 1,
        fixed: [0]
      },
      minuteRadio: 1,
      minuteForm: {
        default: '*',
        start: 0,
        end: 0,
        rangeStart: 0,
        rangeEnd: 1,
        fixed: [0]
      },
      hourRadio: 1,
      hourForm: {
        default: '*',
        start: 0,
        end: 0,
        rangeStart: 0,
        rangeEnd: 1,
        fixed: [0]
      },
      dayRadio: 1,
      dayForm: {
        default: '*',
        start: 0,
        end: 0,
        rangeStart: 0,
        rangeEnd: 1,
        fixed: [1],
        noFixed: '?',
        lastDay: 1,
        workDay: 1,
        lastWorkDay: 'LW'
      },
      monthRadio: 1,
      monthForm: {
        default: '*',
        start: 0,
        end: 0,
        rangeStart: 0,
        rangeEnd: 1,
        fixed: [1]
      },
      weekRadio: 1,
      weekForm: {
        default: '*',
        start: 0,
        end: 0,
        rangeStart: 0,
        rangeEnd: 1,
        fixed: [1],
        noFixed: '?',
        lastWeek: 1,
        monthWeek: 1,
        weekNum: 1
      },
      weekList: [
        { label: '星期天', value: 1, disabled: false },
        { label: '星期一', value: 2, disabled: false },
        { label: '星期二', value: 3, disabled: false },
        { label: '星期三', value: 4, disabled: false },
        { label: '星期四', value: 5, disabled: false },
        { label: '星期五', value: 6, disabled: false },
        { label: '星期六', value: 7, disabled: false }
      ],
      yearRadio: 1,
      nowYear: new Date().getFullYear(),
      yearForm: {
        default: '*',
        start: new Date().getFullYear(),
        end: 1,
        rangeStart: new Date().getFullYear(),
        rangeEnd: new Date().getFullYear(),
        fixed: [new Date().getFullYear()],
        none: ''
      },
      helpForm: '',
      helpList: [
        { label: '每秒', value: '* * * * * ?' },
        { label: '每30分钟', value: '0 */30 * * * ?' },
        { label: '在每小时的第15,30,45分钟', value: '0 15,30,45 * * * ?' },
        { label: '每个偶数小时', value: '0 0 0/2 * * ?' },
        { label: '每个奇数小时', value: '0 0 1/2 * * ?' },
        { label: '每天凌晨12点(12am)', value: '0 0 0 * * ?' },
        { label: '每天中午12点(12pm)', value: '0 0 12 * * ?' },
        { label: '每周一12点', value: '0 0 12 * * MON' },
        { label: '每周一至周五12点', value: '0 0 12 * * MON-FRI' },
        { label: '每月1号开始每隔4天的中午12点', value: '0 0 12 1/4 * ?' },
        { label: '每月最后一天的中午12点', value: '0 0 12 L * ?' },
        {
          label: '每月最后一天前两天(倒数第三天)中午12点',
          value: '0 0 12 L-2 * ?'
        },
        { label: '每月最后一个工作日的12点', value: '0 0 12 LW * ?' },
        { label: '最接近每月1号的那个工作日的12点', value: '0 0 12 1W * ?' },
        { label: '每月最后一个星期天12点', value: '0 0 12 ? * 1L' },
        { label: '每月第一个星期五的12点', value: '0 0 12 ? * 6#1' },
        { label: '1月和6月的每天中午12点', value: '0 0 12 * JAN,JUN ?' }
      ]
    }
  },
  computed: {
    secondValue () {
      if (this.secondRadio === 1) {
        return this.secondForm.default
      } else if (this.secondRadio === 2) {
        return this.secondForm.start + '/' + this.secondForm.end
      } else if (this.secondRadio === 3) {
        return this.secondForm.rangeStart + '-' + this.secondForm.rangeEnd
      } else if (this.secondRadio === 4) {
        return this.secondForm.fixed.toString()
      } else {
        return this.formInline.second
      }
    },
    minuteValue () {
      if (this.minuteRadio === 1) {
        return this.minuteForm.default
      } else if (this.minuteRadio === 2) {
        return this.minuteForm.start + '/' + this.minuteForm.end
      } else if (this.minuteRadio === 3) {
        return this.minuteForm.rangeStart + '-' + this.minuteForm.rangeEnd
      } else if (this.minuteRadio === 4) {
        return this.minuteForm.fixed.toString()
      } else {
        return this.formInline.minute
      }
    },
    hourValue () {
      if (this.hourRadio === 1) {
        return this.hourForm.default
      } else if (this.hourRadio === 2) {
        return this.hourForm.start + '/' + this.hourForm.end
      } else if (this.hourRadio === 3) {
        return this.hourForm.rangeStart + '-' + this.hourForm.rangeEnd
      } else if (this.hourRadio === 4) {
        return this.hourForm.fixed.toString()
      } else {
        return this.formInline.hour
      }
    },
    dayValue () {
      if (this.dayRadio === 1) {
        return this.dayForm.default
      } else if (this.dayRadio === 2) {
        return this.dayForm.start + '/' + this.hourForm.end
      } else if (this.dayRadio === 3) {
        return this.dayForm.rangeStart + '-' + this.hourForm.rangeEnd
      } else if (this.dayRadio === 4) {
        return this.dayForm.fixed.toString()
      } else if (this.dayRadio === 5) {
        return this.dayForm.noFixed
      } else if (this.dayRadio === 6) {
        if (this.dayForm.lastDay === 1) {
          return 'L'
        } else {
          return 'L-' + (this.dayForm.lastDay - 1)
        }
      } else if (this.dayRadio === 7) {
        return this.dayForm.workDay + 'W'
      } else if (this.dayRadio === 8) {
        return this.dayForm.lastWorkDay
      } else {
        return this.formInline.day
      }
    },
    monthValue () {
      if (this.monthRadio === 1) {
        return this.monthForm.default
      } else if (this.monthRadio === 2) {
        return this.monthForm.start + '/' + this.monthForm.end
      } else if (this.monthRadio === 3) {
        return this.monthForm.rangeStart + '-' + this.monthForm.rangeEnd
      } else if (this.monthRadio === 4) {
        return this.monthForm.fixed.toString()
      } else {
        return this.formInline.month
      }
    },
    weekValue () {
      if (this.weekRadio === 1) {
        return this.weekForm.default
      } else if (this.weekRadio === 2) {
        return this.weekForm.start + '/' + this.weekForm.end
      } else if (this.weekRadio === 3) {
        return this.weekForm.rangeStart + '-' + this.weekForm.rangeEnd
      } else if (this.weekRadio === 4) {
        return this.weekForm.fixed.toString()
      } else if (this.weekRadio === 5) {
        return this.weekForm.noFixed
      } else if (this.weekRadio === 6) {
        return this.weekForm.lastWeek + 'L'
      } else if (this.weekRadio === 7) {
        return this.weekForm.weekNum + '#' + this.weekForm.monthWeek
      } else {
        return this.formInline.week
      }
    },
    // eslint-disable-next-line vue/return-in-computed-property
    yearValue () {
      if (this.yearRadio === 1) {
        return this.yearForm.default
      } else if (this.yearRadio === 2) {
        return this.yearForm.start + '/' + this.yearForm.end
      } else if (this.yearRadio === 3) {
        return this.yearForm.rangeStart + '-' + this.yearForm.rangeEnd
      } else if (this.yearRadio === 4) {
        return this.yearForm.fixed.toString()
      } else if (this.yearRadio === 5) {
        return this.yearForm.none
      } else {
        return this.yearForm.none
      }
    }
  },
  watch: {
    secondValue (nv, ov) {
      const res =
        nv +
        ' ' +
        this.minuteValue +
        ' ' +
        this.hourValue +
        ' ' +
        this.dayValue +
        ' ' +
        this.monthValue +
        ' ' +
        this.weekValue +
        ' ' +
        this.yearValue
      this.$emit('input', res)
    },
    minuteValue (nv, ov) {
      const res =
        nv +
        ' ' +
        this.hourValue +
        ' ' +
        this.dayValue +
        ' ' +
        this.monthValue +
        ' ' +
        this.weekValue +
        ' ' +
        this.yearValue
      this.$emit('input', res)
    },
    hourValue (nv, ov) {
      const res =
        this.minuteValue +
        ' ' +
        nv +
        ' ' +
        this.dayValue +
        ' ' +
        this.monthValue +
        ' ' +
        this.weekValue +
        ' ' +
        this.yearValue
      this.$emit('input', res)
    },
    dayValue (nv, ov) {
      const res =
        this.minuteValue +
        ' ' +
        this.hourValue +
        ' ' +
        nv +
        ' ' +
        this.monthValue +
        ' ' +
        this.weekValue +
        ' ' +
        this.yearValue
      this.$emit('input', res)
    },
    monthValue (nv, ov) {
      const res =
        this.minuteValue +
        ' ' +
        this.hourValue +
        ' ' +
        this.dayValue +
        ' ' +
        nv +
        ' ' +
        this.weekValue +
        ' ' +
        this.yearValue
      this.$emit('input', res)
    },
    weekValue (nv, ov) {
      const res =
        this.minuteValue +
        ' ' +
        this.hourValue +
        ' ' +
        this.dayValue +
        ' ' +
        this.monthValue +
        ' ' +
        nv +
        ' ' +
        this.yearValue
      this.$emit('input', res)
    },
    yearValue (nv, ov) {
      const res =
        this.minuteValue +
        ' ' +
        this.hourValue +
        ' ' +
        this.dayValue +
        ' ' +
        this.monthValue +
        ' ' +
        this.weekValue +
        ' ' +
        nv
      this.$emit('input', res)
    }
  },
  methods: {
    tabClick (event) {
      const name = event
      this.tabName = name
      if (name !== 'help') {
        this.$refs[name].focus()
      }
    },
    secondChange (event) {
      this.secondRadio = event
    },
    minuteChange (event) {
      this.minuteRadio = event
    },
    hourChange (event) {
      this.hourRadio = event
    },
    dayChange (event) {
      this.dayRadio = event
    },
    onHelpChange () {
      const helpForm = this.helpForm.split(' ')
      this.secondRadio = 99
      this.formInline.second = helpForm[0]
      this.minuteRadio = 99
      this.formInline.minute = helpForm[1]
      this.hourRadio = 99
      this.formInline.hour = helpForm[2]
      this.dayRadio = 99
      this.formInline.day = helpForm[3]
      this.monthRadio = 99
      this.formInline.month = helpForm[4]
      this.weekRadio = 99
      this.formInline.week = helpForm[5]
    }
  }
}
</script>

<style scoped>
.radio-left {
  text-align: left;
  margin-top: 10px;
}
.color-red {
  color: red;
}
.el-form--inline .el-form-item {
  width: 80px;
  margin-right: 6px;
}
.el-form-item--mini.el-form-item,
.el-form-item--small.el-form-item {
  margin-bottom: 5px;
}
</style>
