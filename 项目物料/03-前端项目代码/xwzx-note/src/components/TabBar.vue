<template>
  <van-tabbar v-model="active" route class="shiyue-tabbar">
    <van-tabbar-item to="/home" icon="records-o">拾页</van-tabbar-item>
    <van-tabbar-item to="/aichat" icon="chat-o">灵感</van-tabbar-item>
    <van-tabbar-item to="/my" icon="manager-o">书桌</van-tabbar-item>
  </van-tabbar>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const active = ref(0)

const setActiveTab = () => {
  const path = route.path
  if (path.includes('/home')) {
    active.value = 0
  } else if (path.includes('/aichat')) {
    active.value = 1
  } else if (path.includes('/my')) {
    active.value = 2
  }
}

watch(() => route.path, setActiveTab, { immediate: true })
</script>

<style scoped>
.shiyue-tabbar {
  height: calc(54px + var(--safe-area-inset-bottom));
}

:deep(.van-tabbar-item) {
  font-size: 12px;
}

:deep(.van-tabbar-item__icon) {
  margin-bottom: 3px;
  font-size: 21px;
}
</style>
