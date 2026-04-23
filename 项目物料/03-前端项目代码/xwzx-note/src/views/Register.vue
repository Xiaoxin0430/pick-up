<template>
  <div class="register-page page-shell">
    <van-nav-bar
      title="加入拾页"
      left-arrow
      fixed
      @click-left="onClickLeft"
    />

    <div class="register-container">
      <div class="brand-card">
        <img class="logo-mark" src="/logo.png" alt="拾页" />
        <p>Start Writing</p>
        <h2>给自己的记录留一个位置</h2>
      </div>

      <van-form @submit="onSubmit" class="register-form">
        <van-cell-group inset>
          <van-field
            v-model="username"
            name="username"
            label="账号"
            placeholder="设置你的账号"
            :rules="[{ required: true, message: '请填写账号' }]"
          />
          <van-field
            v-model="password"
            type="password"
            name="password"
            label="密码"
            placeholder="设置密码"
            :rules="[{ required: true, message: '请填写密码' }]"
          />
          <van-field
            v-model="confirmPassword"
            type="password"
            name="confirmPassword"
            label="确认"
            placeholder="再次输入密码"
            :rules="[
              { required: true, message: '请确认密码' },
              { validator: validatePassword, message: '两次密码不一致' }
            ]"
          />
        </van-cell-group>

        <div class="submit-btn">
          <van-button round block type="primary" native-type="submit" size="large">
            创建书桌
          </van-button>
        </div>

        <div class="login-link">
          已经有书桌？<span @click="goToLogin">去登录</span>
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
const confirmPassword = ref('')

const validatePassword = () => {
  return password.value === confirmPassword.value
}

const onSubmit = async () => {
  showToast({
    type: 'loading',
    message: '正在创建书桌...',
    forbidClick: true,
    duration: 0
  })

  try {
    const result = await userStore.register({
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
      message: '注册失败，请稍后再试'
    })
  }
}

const onClickLeft = () => {
  router.back()
}

const goToLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  padding-top: 46px;
}

.register-container {
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

.register-form {
  width: 100%;
}

.submit-btn {
  margin: 24px 16px;
}

.login-link {
  margin-top: 16px;
  color: var(--ink-muted);
  font-size: 14px;
  text-align: center;
}

.login-link span {
  color: var(--brand-deep);
  font-weight: 700;
}
</style>
