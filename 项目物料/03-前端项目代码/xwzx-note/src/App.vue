<template>
  <div class="app">
    <router-view v-slot="{ Component }">
      <template v-if="$route.meta.keepAlive">
        <keep-alive>
          <component :is="Component" />
        </keep-alive>
      </template>
      <template v-else>
        <component :is="Component" />
      </template>
    </router-view>
  </div>
</template>

<script setup>
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html,
body,
#app {
  min-height: 100%;
  width: 100%;
}

html,
body {
  font-family: "LXGW WenKai", "Noto Serif SC", "Source Han Serif SC", "Songti SC", serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  font-size: 16px;
  background: var(--page-bg);
  color: var(--ink);
}

body {
  overflow-x: hidden;
}

.app {
  max-width: 750px;
  min-height: 100vh;
  margin: 0 auto;
  background:
    radial-gradient(circle at 12% 4%, rgba(210, 184, 152, 0.18), transparent 26rem),
    linear-gradient(180deg, #fffaf2 0%, #f8f1e7 100%);
}

@media screen and (max-width: 750px) {
  html {
    font-size: calc(100vw / 750 * 16);
  }
}
</style>
