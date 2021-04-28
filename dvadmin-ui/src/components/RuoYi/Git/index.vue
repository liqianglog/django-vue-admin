<template>
  <div>
    <svg-icon icon-class="gitee" @click="goto"/>
  </div>
</template>

<script>
export default {
  name: 'RuoYiGit',
  data() {
    return {
      url: 'https://gitee.com/liqianglog/django-vue-admin'
    }
  },
  methods: {
    goto() {
      window.open(this.url)
    }
  }
}
</script>
