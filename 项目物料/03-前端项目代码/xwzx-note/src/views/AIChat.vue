<template>
  <div class="ai-chat-container page-shell">
    <van-nav-bar title="灵感助理" fixed />

    <div class="chat-content">
      <section class="assistant-intro">
        <p>Inspiration</p>
        <h1>把零散想法整理成可写下的一页。</h1>
      </section>

      <div class="messages-container" ref="messagesContainer">
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="['message', message.role === 'user' ? 'user-message' : 'ai-message']"
        >
          <div class="message-content">
            <div v-if="message.role === 'assistant' && message.content === ''" class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <div v-else v-html="formatMessage(message.content)"></div>
          </div>
        </div>
      </div>

      <div class="input-container">
        <van-field
          v-model="userInput"
          rows="1"
          autosize
          type="textarea"
          placeholder="写下一个想法，让它变清楚..."
          class="chat-input"
          @keypress.enter.prevent="sendMessage"
        />
        <van-button
          type="primary"
          class="send-button"
          :disabled="isLoading || !userInput.trim()"
          @click="sendMessage"
        >
          送出
        </van-button>
      </div>
    </div>

    <tab-bar />
  </div>
</template>

<script setup>
import { nextTick, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import * as marked from 'marked'
import DOMPurify from 'dompurify'
import TabBar from '../components/TabBar.vue'
import { aiChatConfig } from '../config/api'
import { useUserStore } from '../store/user'

const messages = ref([
  { role: 'assistant', content: '你好，我是拾页的灵感助理。可以帮你整理想法、润色段落，或者把一段记录改成更安静的文字。' }
])
const userInput = ref('')
const messagesContainer = ref(null)
const isLoading = ref(false)
const router = useRouter()
const userStore = useUserStore()

const getToken = () => {
  if (userStore.token) return userStore.token

  try {
    const persisted = localStorage.getItem('user-store')
    if (!persisted) return ''
    const parsed = JSON.parse(persisted)
    return parsed?.token || ''
  } catch (error) {
    console.warn('读取本地登录态失败:', error)
    return ''
  }
}

const buildAuthHeaders = (token) => ({
  'Content-Type': 'application/json',
  Authorization: `Bearer ${token}`
})

const formatMessage = (content) => {
  if (!content) return ''
  return DOMPurify.sanitize(marked.parse(content))
}

const sendMessage = async () => {
  if (!userInput.value.trim() || isLoading.value) return

  const token = getToken()
  if (!token) {
    showToast('请先登录')
    router.push('/login')
    return
  }

  const userMessage = userInput.value.trim()
  messages.value.push({ role: 'user', content: userMessage })
  userInput.value = ''

  messages.value.push({ role: 'assistant', content: '' })

  await nextTick()
  scrollToBottom()

  isLoading.value = true
  try {
    await fetchAIResponse(userMessage, token)
  } catch (error) {
    console.error('Error fetching AI response:', error)
    messages.value[messages.value.length - 1].content = `发生错误：${error.message || '请检查网络连接或稍后再试'}`
  } finally {
    isLoading.value = false
    await nextTick()
    scrollToBottom()
  }
}

const fetchAIResponse = async (userMessage, token) => {
  try {
    const response = await fetch(aiChatConfig.chatEndpoint, {
      method: 'POST',
      headers: buildAuthHeaders(token),
      body: JSON.stringify({
        message: userMessage
      })
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({}))
      throw new Error(error.detail || `HTTP error! status: ${response.status}`)
    }

    const result = await response.json()

    if (result.code === 200) {
      const aiResponse = typeof result.data === 'string'
        ? result.data
        : result.data?.response

      if (!aiResponse) {
        throw new Error('未获取到 AI 回复内容')
      }

      messages.value[messages.value.length - 1].content = aiResponse
    } else {
      throw new Error(result.message || '响应格式错误')
    }
  } catch (error) {
    console.error('Fetch error:', error)
    throw error
  }
}

const loadHistory = async () => {
  const token = getToken()
  if (!token) return

  try {
    const response = await fetch(`${aiChatConfig.historyEndpoint}?limit=20`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (response.status === 404) {
      return
    }

    if (!response.ok) {
      if (response.status === 401) {
        showToast('登录已过期，请重新登录')
      }
      return
    }

    const result = await response.json()
    if (result.code !== 200 || !Array.isArray(result.data) || result.data.length === 0) {
      return
    }

    const historyMessages = []
    const records = [...result.data].reverse()

    records.forEach((item) => {
      if (item.message) {
        historyMessages.push({ role: 'user', content: item.message })
      }
      if (item.response) {
        historyMessages.push({ role: 'assistant', content: item.response })
      }
    })

    if (historyMessages.length > 0) {
      messages.value = historyMessages
    }
  } catch (error) {
    console.warn('加载聊天历史失败:', error)
  }
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

watch(messages, () => {
  nextTick(scrollToBottom)
}, { deep: true })

onMounted(async () => {
  await loadHistory()
  await nextTick()
  scrollToBottom()
})
</script>

<style scoped>
.ai-chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  padding-top: 46px;
  padding-bottom: 58px;
  box-sizing: border-box;
}

.chat-content {
  display: flex;
  min-height: 0;
  flex: 1;
  flex-direction: column;
  overflow: hidden;
}

.assistant-intro {
  padding: 24px 22px 10px;
}

.assistant-intro p {
  margin: 0 0 8px;
  color: var(--accent);
  font-family: Georgia, "Times New Roman", serif;
  font-size: 12px;
  font-style: italic;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}

.assistant-intro h1 {
  max-width: 18em;
  margin: 0;
  color: var(--ink);
  font-size: 22px;
  line-height: 1.45;
}

.messages-container {
  flex: 1;
  padding: 10px 18px 18px;
  overflow-y: auto;
}

.message {
  max-width: 84%;
  margin-bottom: 14px;
}

.user-message {
  margin-left: auto;
}

.ai-message {
  margin-right: auto;
}

.message-content {
  padding: 13px 15px;
  word-break: break-word;
  border-radius: 20px;
  box-shadow: 0 10px 26px rgba(83, 63, 42, 0.06);
}

.user-message .message-content {
  color: #fffaf2;
  background: var(--brand);
  border-bottom-right-radius: 8px;
}

.ai-message .message-content {
  color: var(--ink);
  background: rgba(255, 253, 248, 0.94);
  border: 1px solid rgba(117, 94, 70, 0.1);
  border-bottom-left-radius: 8px;
}

.input-container {
  display: flex;
  gap: 10px;
  align-items: flex-end;
  padding: 12px 14px;
  background: rgba(255, 253, 248, 0.92);
  border-top: 1px solid rgba(117, 94, 70, 0.1);
  backdrop-filter: blur(18px);
}

.chat-input {
  flex: 1;
  overflow: hidden;
  border: 1px solid rgba(117, 94, 70, 0.1);
  border-radius: 18px;
}

:deep(.chat-input .van-field__control) {
  line-height: 1.6;
}

.send-button {
  min-width: 64px;
  border-radius: 16px;
}

.typing-indicator {
  display: flex;
  padding: 5px;
}

.typing-indicator span {
  display: inline-block;
  width: 8px;
  height: 8px;
  margin: 0 2px;
  background-color: rgba(139, 111, 82, 0.45);
  border-radius: 50%;
  animation: bounce 1.5s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%,
  60%,
  100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-5px);
  }
}

:deep(pre) {
  padding: 12px;
  overflow-x: auto;
  background-color: #f2e8da;
  border-radius: 12px;
}

:deep(code) {
  padding: 2px 4px;
  font-family: "SFMono-Regular", Consolas, monospace;
  background-color: rgba(139, 111, 82, 0.1);
  border-radius: 5px;
}

:deep(p) {
  margin: 8px 0;
  line-height: 1.75;
}

:deep(ul),
:deep(ol) {
  padding-left: 20px;
}

:deep(a) {
  color: var(--brand-deep);
  text-decoration: none;
}
</style>
