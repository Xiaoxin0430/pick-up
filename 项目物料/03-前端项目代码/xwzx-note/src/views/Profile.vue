<template>
  <div class="profile-page page-shell">
    <van-nav-bar
      title="书桌资料"
      left-arrow
      fixed
      @click-left="$router.back()"
    />

    <div class="profile-container">
      <section class="profile-hero">
        <van-image
          round
          width="72"
          height="72"
          src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
        />
        <div>
          <p>Personal Desk</p>
          <h1>{{ userInfo.username || 'admin' }}</h1>
        </div>
      </section>

      <van-cell-group inset class="info-group">
        <van-cell title="账号" :value="userInfo.username || 'admin'" />
        <van-cell title="书桌编号" :value="`ID: shiye-${userId || 'N/A'}`" />
        <van-cell title="个人签名" :value="userBio || '还没有写下签名'" is-link @click="showBioDialog" />
      </van-cell-group>

      <van-cell-group inset class="security-group">
        <van-cell title="修改密码" label="保护你的私人记录" is-link @click="showPasswordConfirm" />
      </van-cell-group>
    </div>
  </div>
</template>

<script setup>
import { computed, h, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { showDialog, showFailToast, showLoadingToast, showSuccessToast, showToast } from 'vant'
import { useUserStore } from '../store/user'

const router = useRouter()
const userStore = useUserStore()

onMounted(async () => {
  if (!userStore.getLoginStatus) {
    router.push('/login')
    return
  }

  try {
    const loadingInstance = showLoadingToast({
      message: '正在整理资料...',
      forbidClick: true,
      duration: 0
    })

    const result = await userStore.getUserInfoDetail()
    loadingInstance.close()

    if (!result.success) {
      showFailToast(result.message || '获取资料失败')
    }
  } catch (error) {
    console.error('获取用户信息请求失败:', error)
    showToast.clear()
    showFailToast('获取资料失败')
  }
})

const userInfo = computed(() => userStore.userInfo)
const userId = computed(() => userStore.token ? userStore.token.substring(0, 5) : '')
const userBio = computed(() => userStore.userInfo?.bio || '还没有写下签名')

const showPasswordConfirm = () => {
  const oldPassword = ref('')
  const newPassword = ref('')
  const confirmPassword = ref('')

  showDialog({
    title: '修改密码',
    showCancelButton: true,
    className: 'password-dialog',
    message: h('div', { style: 'text-align: left; padding: 10px 0;' }, [
      h('div', { style: 'margin-bottom: 15px;' }, [
        h('div', { style: 'margin-bottom: 5px; text-align: left;' }, '当前密码：'),
        h('input', {
          type: 'password',
          value: oldPassword.value,
          onInput: (e) => { oldPassword.value = e.target.value },
          style: 'width: 100%; border: 1px solid #dcdee0; border-radius: 12px; padding: 10px; box-sizing: border-box;'
        })
      ]),
      h('div', { style: 'margin-bottom: 15px;' }, [
        h('div', { style: 'margin-bottom: 5px; text-align: left;' }, '新密码：'),
        h('input', {
          type: 'password',
          value: newPassword.value,
          onInput: (e) => { newPassword.value = e.target.value },
          style: 'width: 100%; border: 1px solid #dcdee0; border-radius: 12px; padding: 10px; box-sizing: border-box;'
        })
      ]),
      h('div', { style: 'margin-bottom: 15px;' }, [
        h('div', { style: 'margin-bottom: 5px; text-align: left;' }, '确认密码：'),
        h('input', {
          type: 'password',
          value: confirmPassword.value,
          onInput: (e) => { confirmPassword.value = e.target.value },
          style: 'width: 100%; border: 1px solid #dcdee0; border-radius: 12px; padding: 10px; box-sizing: border-box;'
        })
      ])
    ]),
  }).then(async () => {
    if (!oldPassword.value) {
      showToast('请输入当前密码')
      return
    }

    if (!newPassword.value) {
      showToast('请输入新密码')
      return
    }

    if (newPassword.value !== confirmPassword.value) {
      showToast('两次密码输入不一致')
      return
    }

    try {
      const loadingInstance = showLoadingToast({
        message: '正在保存...',
        forbidClick: true,
        duration: 0
      })

      const result = await userStore.updatePassword(oldPassword.value, newPassword.value)
      loadingInstance.close()

      if (result && result.success) {
        showSuccessToast('密码修改成功')
      } else {
        showFailToast((result && result.message) || '密码修改失败')
      }
    } catch (error) {
      console.error('修改密码失败:', error)
      showToast.clear()
      showFailToast('密码修改失败')
    }
  }).catch(() => {})
}

const showBioDialog = () => {
  const newBioValue = ref(userBio.value)

  showDialog({
    title: '修改个人签名',
    showCancelButton: true,
    confirmButtonText: '保存',
    className: 'bio-dialog',
    message: h('div', { style: 'text-align: left; padding: 10px 0;' }, [
      h('div', { style: 'margin-bottom: 15px;' }, [
        h('div', { style: 'margin-bottom: 5px; text-align: left;' }, '个人签名：'),
        h('textarea', {
          value: newBioValue.value,
          onInput: (e) => { newBioValue.value = e.target.value },
          style: 'width: 100%; border: 1px solid #dcdee0; border-radius: 12px; padding: 10px; box-sizing: border-box; min-height: 100px; resize: vertical;'
        })
      ])
    ])
  }).then(async () => {
    try {
      const loadingInstance = showLoadingToast({
        message: '正在保存...',
        forbidClick: true,
        duration: 0
      })

      const result = await userStore.updateUserBio(newBioValue.value)
      loadingInstance.close()

      if (result && result.success) {
        showSuccessToast('个人签名已更新')
      } else {
        showFailToast((result && result.message) || '保存失败')
      }
    } catch (error) {
      console.error('更新个人简介失败:', error)
      showToast.clear()
      showFailToast('保存失败')
    }
  }).catch(() => {})
}
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  padding-top: 46px;
}

.profile-container {
  padding: 24px 18px 28px;
}

.profile-hero {
  display: flex;
  gap: 16px;
  align-items: center;
  margin-bottom: 18px;
  padding: 22px;
  background: rgba(255, 253, 248, 0.92);
  border: 1px solid rgba(117, 94, 70, 0.1);
  border-radius: 28px;
  box-shadow: var(--shadow);
}

.profile-hero p {
  margin: 0 0 6px;
  color: var(--accent);
  font-family: Georgia, "Times New Roman", serif;
  font-size: 12px;
  font-style: italic;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.profile-hero h1 {
  margin: 0;
  color: var(--ink);
  font-size: 24px;
}

.info-group,
.security-group {
  margin-top: 14px;
}

:deep(.van-cell) {
  padding: 17px 16px;
}

:deep(.van-cell__title) {
  color: var(--ink);
  font-weight: 700;
}
</style>
