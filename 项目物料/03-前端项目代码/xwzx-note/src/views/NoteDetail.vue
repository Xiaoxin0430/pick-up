<template>
  <div class="note-detail page-shell">
    <van-nav-bar
      title="笔记正文"
      left-text="返回"
      left-arrow
      fixed
      @click-left="onClickLeft"
    />

    <main class="detail-content" v-if="noteStore.noteDetail.id">
      <header class="note-header">
        <div class="header-meta">
          <span>{{ noteTag }}</span>
          <span>{{ noteTime }}</span>
          <span>{{ noteStore.noteDetail.views || 0 }} 次翻阅</span>
        </div>

        <div class="title-container">
          <h1 class="title">{{ noteStore.noteDetail.title }}</h1>
          <van-button
            class="favorite-btn"
            :icon="isFavorite ? 'star' : 'star-o'"
            :class="{ 'is-favorite': isFavorite }"
            @click="toggleFavorite"
          />
        </div>

        <p class="summary" v-if="noteStore.noteDetail.description">
          {{ noteStore.noteDetail.description }}
        </p>
      </header>

      <figure class="cover" v-if="noteStore.noteDetail.image">
        <img :src="noteStore.noteDetail.image" :alt="`笔记配图：${noteStore.noteDetail.title}`">
      </figure>

      <article class="content">
        <p v-for="(paragraph, index) in contentParagraphs" :key="index">
          {{ paragraph }}
        </p>
      </article>

      <section class="related-notes" v-if="noteStore.noteDetail.relatedNote?.length">
        <div class="section-title">
          <span>继续翻阅</span>
          <small>同一分类里的几页记录</small>
        </div>

        <div class="related-list">
          <div
            class="related-item"
            v-for="item in noteStore.noteDetail.relatedNote"
            :key="item.id"
            @click="goToRelatedNote(item.id)"
          >
            <div class="related-image">
              <img :src="item.image" :alt="`笔记配图：${item.title}`">
            </div>
            <div class="related-copy">
              <div class="related-title">{{ item.title }}</div>
              <span>翻到这一页</span>
            </div>
          </div>
        </div>
      </section>
    </main>

    <van-empty v-else description="正在铺开这一页..." />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showToast } from 'vant'
import { useNoteStore } from '../store/modules/note'
import { useHistoryStore } from '../store/modules/history'
import { useFavoriteStore } from '../store/modules/favorite'
import { useUserStore } from '../store/user'

const route = useRoute()
const router = useRouter()
const noteStore = useNoteStore()
const historyStore = useHistoryStore()
const favoriteStore = useFavoriteStore()
const userStore = useUserStore()

const noteId = computed(() => Number(route.params.id))

const noteTag = computed(() => noteStore.noteDetail.author || '未分类')
const noteTime = computed(() => (
  noteStore.noteDetail.publishTime ||
  noteStore.noteDetail.publishedTime ||
  noteStore.noteDetail.publish_time ||
  '刚刚更新'
))

const contentParagraphs = computed(() => {
  if (!noteStore.noteDetail.content) return []
  return noteStore.noteDetail.content
    .split(/\n{1,}/)
    .map(paragraph => paragraph.trim())
    .filter(Boolean)
})

const onClickLeft = () => {
  router.back()
}

const goToRelatedNote = (id) => {
  router.push(`/note/detail/${id}`)
}

const isFavorite = computed(() => {
  return favoriteStore.isFavorite(noteId.value)
})

const toggleFavorite = async () => {
  if (!userStore.getLoginStatus) {
    showToast({
      message: '登录后才能把这一页放入收藏',
      position: 'bottom',
    })
    router.push('/login')
    return
  }

  const status = await favoriteStore.toggleFavorite(noteStore.noteDetail)

  if (status === true) {
    showToast({
      message: '已收进收藏夹',
      position: 'bottom',
    })
  } else if (status === false) {
    showToast({
      message: '已从收藏夹移出',
      position: 'bottom',
    })
  } else {
    showToast({
      message: '操作失败，请稍后再试',
      position: 'bottom',
    })
  }
}

onMounted(async () => {
  await noteStore.getNoteDetail(noteId.value)

  if (noteStore.noteDetail.id) {
    if (userStore.getLoginStatus) {
      try {
        const result = await historyStore.addHistoryApi(noteStore.noteDetail.id)
        console.log('记录浏览历史API结果:', result)
      } catch (error) {
        console.error('记录浏览历史API失败:', error)
      }
    }
  }

  favoriteStore.loadFavorites()

  if (userStore.getLoginStatus && noteStore.noteDetail.id) {
    const result = await favoriteStore.checkFavoriteStatusApi(noteStore.noteDetail.id)
    if (result.success && !result.isLocal) {
      if (result.isFavorite && !favoriteStore.isFavorite(noteStore.noteDetail.id)) {
        favoriteStore.addFavorite(noteStore.noteDetail)
      } else if (!result.isFavorite && favoriteStore.isFavorite(noteStore.noteDetail.id)) {
        favoriteStore.removeFavorite(noteStore.noteDetail.id)
      }
    }
  }
})
</script>

<style scoped>
.note-detail {
  min-height: 100vh;
  padding-top: 46px;
  padding-bottom: 38px;
}

.detail-content {
  max-width: 680px;
  margin: 0 auto;
  padding: 24px 18px 0;
}

.note-header {
  padding: 24px 20px 22px;
  background: rgba(255, 253, 248, 0.94);
  border: 1px solid rgba(117, 94, 70, 0.1);
  border-radius: 30px;
  box-shadow: var(--shadow);
}

.header-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 18px;
  color: var(--ink-muted);
  font-size: 12px;
}

.header-meta span {
  padding: 4px 10px;
  background: rgba(139, 111, 82, 0.08);
  border-radius: 999px;
}

.title-container {
  display: flex;
  align-items: flex-start;
  gap: 14px;
}

.title {
  flex: 1;
  margin: 0;
  color: var(--ink);
  font-size: 30px;
  font-weight: 700;
  line-height: 1.3;
  letter-spacing: 0.01em;
}

.favorite-btn {
  flex-shrink: 0;
  width: 42px;
  height: 42px;
  padding: 0;
  color: var(--brand);
  background: var(--paper-soft);
  border: 1px solid rgba(117, 94, 70, 0.12);
  border-radius: 50%;
}

.favorite-btn.is-favorite {
  color: #b2783f;
  background: #f6e7d4;
}

.summary {
  margin: 18px 0 0;
  padding-left: 14px;
  color: var(--ink-soft);
  font-size: 15px;
  line-height: 1.9;
  border-left: 3px solid rgba(139, 111, 82, 0.28);
}

.cover {
  margin: 22px 0 0;
  overflow: hidden;
  background: var(--paper-warm);
  border-radius: 30px;
  box-shadow: var(--shadow);
}

.cover img {
  display: block;
  width: 100%;
  max-height: 420px;
  object-fit: cover;
  filter: saturate(0.88) contrast(0.98);
}

.content {
  margin-top: 26px;
  padding: 28px 22px;
  color: #3b332a;
  background: rgba(255, 253, 248, 0.78);
  border: 1px solid rgba(117, 94, 70, 0.08);
  border-radius: 30px;
}

.content p {
  margin: 0 0 18px;
  font-size: 17px;
  line-height: 2.05;
  letter-spacing: 0.015em;
  text-align: justify;
}

.content p:last-child {
  margin-bottom: 0;
}

.content p:first-child::first-letter {
  color: var(--brand-deep);
  font-size: 2.2em;
  font-weight: 700;
  line-height: 1;
}

.related-notes {
  margin-top: 30px;
}

.section-title {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 14px;
  padding: 0 4px;
}

.section-title span {
  color: var(--ink);
  font-size: 18px;
  font-weight: 700;
}

.section-title small {
  color: var(--ink-muted);
  font-size: 12px;
}

.related-list {
  display: grid;
  gap: 12px;
}

.related-item {
  display: grid;
  grid-template-columns: 72px minmax(0, 1fr);
  gap: 14px;
  padding: 12px;
  background: rgba(255, 253, 248, 0.9);
  border: 1px solid rgba(117, 94, 70, 0.09);
  border-radius: 22px;
}

.related-image {
  width: 72px;
  height: 72px;
  overflow: hidden;
  border-radius: 18px;
}

.related-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.related-copy {
  display: flex;
  min-width: 0;
  flex-direction: column;
  justify-content: center;
}

.related-title {
  display: -webkit-box;
  overflow: hidden;
  color: var(--ink);
  font-size: 15px;
  font-weight: 700;
  line-height: 1.5;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  line-clamp: 2;
}

.related-copy span {
  margin-top: 6px;
  color: var(--ink-muted);
  font-size: 12px;
}
</style>
