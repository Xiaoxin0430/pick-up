<template>
  <div class="my-container page-shell">
    <van-nav-bar title="我的书桌" fixed />

    <section class="desk-card" @click="goToProfile" v-if="isLogin">
      <div class="avatar-mark">
        <van-image
          round
          width="74"
          height="74"
          src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
        />
      </div>
      <div class="desk-info">
        <p>正在记录</p>
        <h1>{{ userInfo.username }}</h1>
        <span>{{ userBio || '这个人还没有写下简介。' }}</span>
      </div>
      <van-icon name="arrow" class="arrow-icon" />
    </section>

    <section class="desk-card guest-card" v-else>
      <div class="avatar-mark">
        <van-image
          round
          width="74"
          height="74"
          src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
        />
      </div>
      <div class="desk-info">
        <p>欢迎来到拾页</p>
        <h1>还未登录</h1>
        <span>登录后同步收藏与翻阅记录。</span>
      </div>
      <div class="guest-actions">
        <van-button round size="small" type="primary" @click="goToLogin">登录</van-button>
        <van-button round size="small" plain @click="goToRegister">注册</van-button>
      </div>
    </section>

    <div class="menu-list">
      <van-cell-group inset>
        <van-cell title="收藏夹" label="舍不得删掉的页" icon="star-o" is-link @click="goToFavorite" />
        <van-cell title="翻阅记录" label="最近读过的笔记" icon="underway-o" is-link @click="goToHistory" />
        <van-cell title="提醒" label="暂时安静，没有新提醒" icon="bell-o" is-link />
        <van-cell title="偏好设置" label="语言、主题与账户" icon="setting-o" is-link @click="goToSettings" />
        <van-cell v-if="isLogin" title="退出登录" icon="close" @click="handleLogout" />
      </van-cell-group>
    </div>

    <tab-bar />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showDialog, showToast } from 'vant'
import { useUserStore } from '../store/user'
import TabBar from '../components/TabBar.vue'

const userStore = useUserStore()
const router = useRouter()

const userInfo = computed(() => userStore.userInfo)
const isLogin = computed(() => userStore.getLoginStatus)
const userBio = computed(() => userStore.getUserBio || userStore.userInfo?.bio)

const goToLogin = () => {
  router.push('/login')
}

const goToRegister = () => {
  router.push('/register')
}

const goToProfile = () => {
  if (isLogin.value) {
    router.push('/profile')
  }
}

const goToHistory = () => {
  if (isLogin.value) {
    router.push('/history')
  } else {
    showToast('请先登录')
    router.push('/login')
  }
}

const goToFavorite = () => {
  if (isLogin.value) {
    router.push('/favorite')
  } else {
    showToast('请先登录')
    router.push('/login')
  }
}

const goToSettings = () => {
  router.push('/settings')
}

const handleLogout = () => {
  showDialog({
    title: '确认退出',
    message: '要离开当前书桌吗？',
    showCancelButton: true,
  }).then((action) => {
    if (action === 'confirm') {
      userStore.logout()
      router.push('/login')
    }
  })
}

onMounted(async () => {
  try {
    await userStore.getUserInfoDetail()
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
})
</script>

<style scoped>
.my-container {
  min-height: 100vh;
  padding-top: 46px;
  padding-bottom: 78px;
}

.desk-card {
  position: relative;
  display: grid;
  grid-template-columns: 74px minmax(0, 1fr) 22px;
  gap: 16px;
  align-items: center;
  margin: 26px 18px 18px;
  padding: 20px;
  overflow: hidden;
  background:
    radial-gradient(circle at 92% 14%, rgba(185, 130, 88, 0.16), transparent 8rem),
    rgba(255, 253, 248, 0.94);
  border: 1px solid rgba(117, 94, 70, 0.1);
  border-radius: 30px;
  box-shadow: var(--shadow);
}

.guest-card {
  grid-template-columns: 74px minmax(0, 1fr);
}

.avatar-mark {
  padding: 4px;
  background: rgba(139, 111, 82, 0.12);
  border-radius: 50%;
}

.desk-info {
  min-width: 0;
}

.desk-info p {
  margin: 0 0 5px;
  color: var(--accent);
  font-family: Georgia, "Times New Roman", serif;
  font-size: 12px;
  font-style: italic;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.desk-info h1 {
  margin: 0;
  color: var(--ink);
  font-size: 24px;
  line-height: 1.3;
}

.desk-info span {
  display: -webkit-box;
  margin-top: 7px;
  overflow: hidden;
  color: var(--ink-soft);
  font-size: 13px;
  line-height: 1.5;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  line-clamp: 2;
}

.arrow-icon {
  color: var(--ink-muted);
}

.guest-actions {
  grid-column: 1 / -1;
  display: flex;
  gap: 10px;
  margin-top: 4px;
}

.menu-list {
  margin: 0 18px;
}

:deep(.van-cell) {
  padding: 17px 16px;
}

:deep(.van-cell__title) {
  color: var(--ink);
  font-weight: 700;
}

:deep(.van-cell__label) {
  color: var(--ink-muted);
}

:deep(.van-cell__left-icon) {
  color: var(--brand);
}
</style>
