<!--
@description: 封装组件, 通用图标组件(已注册全局组件)
用法:<common-icon value="el:el-icon-delete-solid"/>
用法:<common-icon value="svg:icon-folder"/>
-->
<template>
  <!--<svg v-if="iconType && iconType.toLocaleLowerCase() === 'svg'" :class="commonClass" aria-hidden="true">
    <use :xlink:href="commonName"/>
  </svg>-->
  <span>
    <slot name="prepend"/>
    <svg v-if="iconType && iconType.toLocaleLowerCase() === 'svg'" :class="commonClass" aria-hidden="true">
      <use :xlink:href="commonName"/>
    </svg>
    <i v-if="iconType && iconType.toLocaleLowerCase() === 'el'" :class="commonClass"/>
    <span v-if="showTitle">{{ iconTitle }}</span>
    <slot name="append"/>
  </span>
</template>

<script>
export default {
  name: 'CommonIcon',
  props: {
    value: {
      type: String,
      default: ''
    },
    iconTitle: {
      type: String,
      default: ''
    },
    iconClass: {
      type: String,
      required: false,
      default: ''
    },
    showTitle: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      iconType: '',
      iconName: '',
      commonName: '',
      commonClass: ''
    };
  },
  computed: {
  },
  watch: {
    value(val) {
      this.change(val);
    }
  },
  created() {
  },
  mounted() {
    this.change(this.value);
  },
  methods: {
    change(val) {
      const arr = val.split(':');
      if (arr.length >= 2) {
        this.iconType = arr[0];
        this.iconName = arr[1];
      } else {
        this.iconType = '';
        this.iconName = '';
      }
      this.commonName = this.getCommonName();
      this.commonClass = this.getCommonClass();
    },
    getCommonName() {
      if (this.iconType && this.iconType.toLocaleLowerCase() === 'svg') {
        return `#icon-${this.iconName}`;
      }
      if (this.iconType && this.iconType.toLocaleLowerCase() === 'el') {
        return `${this.iconName}`;
      }
      return '';
    },
    getCommonClass() {
      if (this.iconType && this.iconType.toLocaleLowerCase() === 'svg') {
        if (this.className) {
          return 'svg-icon ' + this.className;
        } else {
          return 'svg-icon';
        }
      }
      if (this.iconType && this.iconType.toLocaleLowerCase() === 'el') {
        if (this.className) {
          return this.iconName + ' ' + this.className;
        } else {
          return this.iconName;
        }
      }
      return '';
    }
  }
};
</script>

<style scoped>
.svg-icon {
  width: 1em;
  height: 1em;
  vertical-align: -0.15em;
  fill: currentColor;
  overflow: hidden;
}
</style>
