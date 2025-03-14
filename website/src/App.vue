<template>
  <div id="app" class="text-center bg-background bg-stone-100">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      colorTheme: "stone",
      darkmod: false
    }
  }
};
</script>

<style>
/* 你可以在这里添加自定义样式 */
</style>
