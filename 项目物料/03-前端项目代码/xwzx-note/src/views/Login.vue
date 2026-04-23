<template>
  <div class="login-page page-shell">
    <van-nav-bar
      title="登录拾页"
      left-arrow
      fixed
      @click-left="onClickLeft"
    />

    <div class="login-container">
      <div class="brand-card">
        <img class="logo-mark" src="/logo.png" alt="拾页" />
        <p>Shiye Notes</p>
        <h2>回到你的私人书桌</h2>
      </div>

      <van-form @submit="onSubmit" class="login-form">
        <van-cell-group inset>
          <van-field
            v-model="username"
            name="username"
            label="账号"
            placeholder="请输入账号"
            :rules="[{ required: true, message: '请填写账号' }]"
          />
          <van-field
            v-model="password"
            type="password"
            name="password"
            label="密码"
            placeholder="请输入密码"
            :rules="[{ required: true, message: '请填写密码' }]"
          />
        </van-cell-group>

        <div class="submit-btn">
          <van-button round block type="primary" native-type="submit" size="large">
            登录
          </van-button>
        </div>

        <div class="login-tips">
          <p>测试账号：admin</p>
          <p>测试密码：123456</p>
        </div>
      </van-form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import { useUserStore } from '../store/user'

const router = useRouter()
const userStore = useUserStore()

const username = ref('')
const password = ref('')

const onSubmit = async () => {
  showToast({
    type: 'loading',
    message: '正在进入书桌...',
    forbidClick: true,
    duration: 0
  })

  try {
    const result = await userStore.login({
      username: username.value,
      password: password.value
    })

    if (result.success) {
      showToast({
        type: 'success',
        message: result.message
      })

      router.push('/')
    } else {
      showToast({
        type: 'fail',
        message: result.message
      })
    }
  } catch (error) {
    showToast({
      type: 'fail',
      message: '登录失败，请稍后再试'
    })
  }
}

const onClickLeft = () => {
  router.back()
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  padding-top: 46px;
}

.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 42px 18px 0;
}

.brand-card {
  width: 100%;
  margin-bottom: 28px;
  padding: 30px 20px;
  text-align: center;
  background: rgba(255, 253, 248, 0.92);
  border: 1px solid rgba(117, 94, 70, 0.1);
  border-radius: 30px;
  box-shadow: var(--shadow);
}

.logo-mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 74px;
  height: 74px;
  margin-bottom: 14px;
  object-fit: cover;
  border-radius: 28px;
}

.brand-card p {
  margin: 0 0 8px;
  color: var(--accent);
  font-family: Georgia, "Times New Roman", serif;
  font-size: 12px;
  font-style: italic;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.brand-card h2 {
  margin: 0;
  color: var(--ink);
  font-size: 23px;
}

.login-form {
  width: 100%;
}

.submit-btn {
  margin: 24px 16px;
}

.login-tips {
  margin-top: 14px;
  color: var(--ink-muted);
  font-size: 13px;
  line-height: 1.7;
  text-align: center;
}
</style>
