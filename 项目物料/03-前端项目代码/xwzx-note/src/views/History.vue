<template>
  <div class="history-container page-shell">
    <van-nav-bar
      title="翻阅记录"
      left-text="返回"
      left-arrow
      right-text="清空"
      fixed
      @click-left="onClickLeft"
      @click-right="onClickClear"
    />

    <section class="history-intro">
      <h1>最近翻过</h1>
      <p>从这里回到刚刚停下的那一页。</p>
    </section>

    <div class="history-list" v-if="historyStore.getHistory.length">
      <article class="history-item" v-for="item in historyStore.getHistory" :key="item.id">
        <div class="note-image" v-if="item.image" @click="goToNoteDetail(item.id)">
          <img :src="item.image" :alt="`笔记配图：${item.title}`">
        </div>

        <div class="note-info" @click="goToNoteDetail(item.id)">
          <div class="note-tag">{{ item.author || '未分类' }}</div>
          <h2>{{ item.title }}</h2>
          <div class="note-meta">
            <span>{{ item.publishTime || item.publishedTime || '刚刚更新' }}</span>
            <span v-if="item.viewTime || item.historyTime">翻阅于 {{ item.viewTime || item.historyTime }}</span>
          </div>
        </div>

        <van-button
          class="delete-btn"
          type="default"
          size="mini"
          icon="cross"
          @click="confirmDelete(item.id)"
        />
      </article>
    </div>

    <van-empty v-else description="还没有翻阅记录" />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showDialog } from 'vant'
import { useHistoryStore } from '../store/modules/history'

const router = useRouter()
const historyStore = useHistoryStore()

const onClickLeft = () => {
  router.back()
}

const goToNoteDetail = (id) => {
  router.push(`/note/detail/${id}`)
}

const removeHistory = async (id) => {
  try {
    const result = await historyStore.removeHistoryApi(id)
    console.log('删除单条历史记录结果:', result)

    if (!result.success && !result.isLocal) {
      showDialog({
        title: '提示',
        message: result.message || '删除失败，请稍后重试',
      })
    }
  } catch (error) {
    console.error('删除历史记录失败:', error)
  }
}

const confirmDelete = (id) => {
  showDialog({
    title: '移出记录',
    message: '确定要删除这条翻阅记录吗？',
    showCancelButton: true,
  }).then((action) => {
    if (action === 'confirm') {
      removeHistory(id)
    }
  })
}

const onClickClear = async () => {
  showDialog({
    title: '清空翻阅记录',
    message: '确定要清空所有翻阅记录吗？',
    showCancelButton: true,
  }).then(async (action) => {
    if (action === 'confirm') {
      try {
        const result = await historyStore.clearHistoryApi()
        console.log('清空历史记录结果:', result)

        if (!result.success && !result.isLocal) {
          showDialog({
            title: '提示',
            message: result.message || '清空失败，请稍后重试',
          })
        }
      } catch (error) {
        console.error('清空历史记录失败:', error)
      }
    }
  })
}

onMounted(async () => {
  try {
    const result = await historyStore.getHistoryListApi()
    console.log('浏览历史页面：API获取结果', result)

    if (!result || !result.success) {
      historyStore.loadHistory()
    }
  } catch (error) {
    console.error('浏览历史页面：API请求异常', error)
    historyStore.loadHistory()
  }
})
</script>

<style scoped>
.history-container {
  min-height: 100vh;
  padding-top: 46px;
  padding-bottom: 24px;
}

.history-intro {
  padding: 30px 22px 12px;
}

.history-intro h1 {
  margin: 0 0 10px;
  color: var(--ink);
  font-size: 28px;
  line-height: 1.3;
}

.history-intro p {
  color: var(--ink-soft);
  font-size: 14px;
}

.history-list {
  display: grid;
  gap: 14px;
  padding: 12px 18px 26px;
}

.history-item {
  position: relative;
  display: grid;
  grid-template-columns: 96px minmax(0, 1fr);
  gap: 14px;
  min-height: 118px;
  padding: 14px 48px 14px 14px;
  background: rgba(255, 253, 248, 0.92);
  border: 1px solid rgba(117, 94, 70, 0.1);
  border-radius: 24px;
  box-shadow: 0 14px 34px rgba(83, 63, 42, 0.07);
}

.note-image {
  width: 96px;
  height: 96px;
  overflow: hidden;
  border-radius: 20px;
  background: var(--paper-warm);
}

.note-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: saturate(0.88);
}

.note-info {
  min-width: 0;
}

.note-tag {
  display: inline-flex;
  max-width: 8em;
  margin-bottom: 8px;
  padding: 3px 9px;
  overflow: hidden;
  color: var(--brand-deep);
  font-size: 12px;
  text-overflow: ellipsis;
  white-space: nowrap;
  background: rgba(139, 111, 82, 0.1);
  border-radius: 999px;
}

.note-info h2 {
  display: -webkit-box;
  margin: 0;
  overflow: hidden;
  color: var(--ink);
  font-size: 16px;
  line-height: 1.5;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  line-clamp: 2;
}

.note-meta {
  display: flex;
  flex-direction: column;
  gap: 3px;
  margin-top: 8px;
  color: var(--ink-muted);
  font-size: 12px;
}

.delete-btn {
  position: absolute;
  top: 50%;
  right: 14px;
  width: 28px;
  height: 28px;
  padding: 0;
  color: var(--ink-muted);
  background: var(--paper-soft);
  border: 1px solid rgba(117, 94, 70, 0.1);
  border-radius: 50%;
  transform: translateY(-50%);
}
</style>
