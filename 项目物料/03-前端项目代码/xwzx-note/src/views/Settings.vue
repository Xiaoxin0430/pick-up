<template>
  <div class="settings-container page-shell">
    <van-nav-bar
      title="偏好设置"
      left-arrow
      fixed
      @click-left="onClickLeft"
    />

    <div class="settings-list">
      <van-cell-group inset title="书写偏好">
        <van-cell title="主题气质" label="选择更适合阅读的色调" is-link @click="showThemePopup = true" />
        <van-cell title="语言" label="界面语言设置" is-link @click="showLanguagePopup = true" />
      </van-cell-group>

      <van-cell-group inset title="账号与隐私">
        <van-cell title="隐私设置" label="管理你的私人记录权限" is-link />
        <van-cell title="提醒设置" label="减少打扰，保持安静" is-link />
        <van-cell title="关于拾页" label="一个安静的个人记录平台" is-link />
      </van-cell-group>
    </div>

    <van-popup
      v-model:show="showThemePopup"
      position="bottom"
      round
      :style="{ height: '40%' }"
    >
      <div class="popup-title">选择主题</div>
      <div class="theme-list">
        <div
          v-for="theme in themeList"
          :key="theme.id"
          class="theme-item"
          :class="{ active: currentTheme === theme.id }"
          @click="changeTheme(theme.id)"
        >
          <div class="theme-color" :style="{ backgroundColor: theme.primaryColor }"></div>
          <div class="theme-name">{{ theme.name }}</div>
        </div>
      </div>
    </van-popup>

    <van-popup
      v-model:show="showLanguagePopup"
      position="bottom"
      round
      :style="{ height: '40%' }"
    >
      <div class="popup-title">选择语言</div>
      <van-radio-group v-model="currentLanguage">
        <van-cell-group inset>
          <van-cell
            v-for="lang in languageOptions"
            :key="lang.value"
            :title="lang.label"
            clickable
            :class="{ 'language-active': currentLanguage === lang.value }"
            @click="currentLanguage = lang.value"
          >
            <template #right-icon>
              <van-radio :name="lang.value" />
            </template>
          </van-cell>
        </van-cell-group>
      </van-radio-group>
      <div class="popup-footer">
        <van-button type="primary" block @click="changeLanguage">确认</van-button>
      </div>
    </van-popup>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import { useI18n } from 'vue-i18n'
import { useThemeStore } from '../store/theme'
import { useLanguageStore } from '../store/language'

const router = useRouter()
const themeStore = useThemeStore()
const languageStore = useLanguageStore()
const { locale } = useI18n()

const onClickLeft = () => {
  router.back()
}

const showThemePopup = ref(false)
const themeList = computed(() => themeStore.getAllThemes)
const currentTheme = computed(() => themeStore.getCurrentTheme)

const changeTheme = (themeId) => {
  themeStore.setTheme(themeId)
  showToast('主题已更改')
  showThemePopup.value = false
}

const showLanguagePopup = ref(false)
const currentLanguage = ref(languageStore.getCurrentLanguage)
const languageOptions = [
  { label: '简体中文', value: 'zh-CN' },
  { label: 'English', value: 'en-US' }
]

const changeLanguage = () => {
  languageStore.setLanguage(currentLanguage.value)
  locale.value = currentLanguage.value
  showLanguagePopup.value = false
  showToast('语言设置已更改')
  window.location.reload()
}
</script>

<style scoped>
.settings-container {
  min-height: 100vh;
  padding-top: 46px;
  padding-bottom: 24px;
}

.settings-list {
  display: grid;
  gap: 18px;
  padding: 24px 0 0;
}

:deep(.van-cell-group__title) {
  color: var(--ink-muted);
  font-size: 13px;
}

:deep(.van-cell) {
  padding: 17px 16px;
}

:deep(.van-cell__title) {
  color: var(--ink);
  font-weight: 700;
}

.popup-title {
  padding: 18px;
  color: var(--ink);
  font-size: 17px;
  font-weight: 700;
  text-align: center;
  border-bottom: 1px solid rgba(117, 94, 70, 0.1);
}

.theme-list {
  display: flex;
  flex-wrap: wrap;
  padding: 18px;
}

.theme-item {
  display: flex;
  width: 25%;
  margin-bottom: 16px;
  cursor: pointer;
  flex-direction: column;
  align-items: center;
}

.theme-color {
  width: 42px;
  height: 42px;
  margin-bottom: 8px;
  border: 2px solid transparent;
  border-radius: 50%;
}

.theme-item.active .theme-color {
  border-color: var(--brand-deep);
}

.theme-name {
  color: var(--ink-soft);
  font-size: 12px;
}

.popup-footer {
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  padding: 16px;
}

.language-active {
  background-color: var(--paper-soft);
}
</style>
