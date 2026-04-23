<template>
  <div class="home page-shell">
    <van-nav-bar title="拾页" fixed />

    <section class="home-hero">
      <p class="eyebrow">Quiet Notes</p>
      <h1>把今天轻轻收进一页</h1>
      <p class="hero-desc">日常、灵感、阅读与片刻心绪，都可以在这里慢慢翻阅。</p>
    </section>

    <div class="category-tabs">
      <van-tabs v-model:active="activeTab" sticky swipeable animated shrink>
        <van-tab
          v-for="(category, index) in displayCategories"
          :key="category.id"
          :title="getCategoryTranslation(category.name, index)"
        >
          <van-pull-refresh
            v-model="noteStore.refreshing"
            pulling-text="轻轻下拉，重新整理"
            loosing-text="松手，更新这叠笔记"
            loading-text="正在整理..."
            @refresh="onRefresh"
          >
            <van-list
              v-model:loading="noteStore.loading"
              :finished="noteStore.finished"
              finished-text="一页一页，慢慢记完了"
              loading-text="正在翻页..."
              @load="onLoad"
            >
              <note-item
                v-for="item in noteStore.noteList"
                :key="item.id"
                :note="item"
              />
            </van-list>
          </van-pull-refresh>
        </van-tab>
      </van-tabs>
    </div>

    <button class="floating-category" type="button" @click="goToCategory">
      <van-icon name="apps-o" />
      <span>分类</span>
    </button>

    <tab-bar />
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useNoteStore } from '../store/modules/note'
import NoteItem from '../components/NoteItem.vue'
import TabBar from '../components/TabBar.vue'

const noteStore = useNoteStore()
const router = useRouter()
const route = useRoute()
const activeTab = ref(0)

const displayCategories = computed(() => {
  return noteStore.categories.filter(category => category.name !== '更多')
})

const getCategoryTranslation = (categoryName) => {
  return categoryName
}

const syncActiveTabByCategoryId = (categoryId) => {
  const index = displayCategories.value.findIndex(category => category.id === Number(categoryId))
  if (index !== -1) {
    activeTab.value = index
  }
}

const goToCategory = () => {
  router.push('/category')
}

const onRefresh = () => {
  noteStore.getNoteList(true)
}

const onLoad = () => {
  noteStore.getNoteList()
}

const handleScroll = () => {}

watch(
  () => route.query.categoryId,
  (newCategoryId) => {
    if (newCategoryId) {
      syncActiveTabByCategoryId(newCategoryId)
      noteStore.changeCategory(Number(newCategoryId))
    }
  },
  { immediate: true }
)

watch(activeTab, (newVal) => {
  const category = displayCategories.value[newVal]
  if (category && noteStore.currentCategory !== category.id) {
    noteStore.changeCategory(category.id)
  }
})

onMounted(async () => {
  await noteStore.getCategories()

  if (route.query.categoryId) {
    syncActiveTabByCategoryId(route.query.categoryId)
  }

  if (!noteStore.noteList.length) {
    noteStore.getNoteList()
  }

  window.addEventListener('scroll', handleScroll)
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.home {
  position: relative;
  padding-top: 46px;
  padding-bottom: 78px;
}

.home-hero {
  margin: 0 18px;
  padding: 30px 4px 22px;
}

.eyebrow {
  margin-bottom: 10px;
  color: var(--accent);
  font-family: Georgia, "Times New Roman", serif;
  font-size: 12px;
  font-style: italic;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}

.home-hero h1 {
  max-width: 11em;
  margin: 0;
  color: var(--ink);
  font-size: 31px;
  font-weight: 700;
  line-height: 1.24;
  letter-spacing: 0.02em;
}

.hero-desc {
  max-width: 22em;
  margin-top: 14px;
  color: var(--ink-soft);
  font-size: 14px;
  line-height: 1.8;
}

.category-tabs {
  position: relative;
}

:deep(.van-tabs__wrap) {
  height: 54px;
  padding: 0 12px;
  background: rgba(255, 250, 242, 0.9);
  backdrop-filter: blur(18px);
  border-top: 1px solid rgba(117, 94, 70, 0.06);
  border-bottom: 1px solid rgba(117, 94, 70, 0.08);
}

:deep(.van-tabs__nav) {
  gap: 8px;
  background: transparent;
}

:deep(.van-tab) {
  flex: none;
  min-width: 58px;
  padding: 0 12px;
  color: var(--ink-muted);
  font-size: 14px;
}

:deep(.van-tab--active) {
  color: var(--brand-deep);
  font-weight: 700;
}

:deep(.van-tabs__line) {
  width: 18px;
  height: 3px;
  background: var(--brand);
  border-radius: 999px;
}

:deep(.van-list) {
  padding-top: 18px;
}

.floating-category {
  position: fixed;
  right: calc((100vw - min(100vw, 750px)) / 2 + 16px);
  bottom: calc(74px + var(--safe-area-inset-bottom));
  z-index: 999;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 38px;
  padding: 0 14px;
  color: var(--brand-deep);
  background: rgba(255, 253, 248, 0.9);
  border: 1px solid rgba(117, 94, 70, 0.14);
  border-radius: 999px;
  box-shadow: 0 14px 32px rgba(83, 63, 42, 0.12);
  backdrop-filter: blur(18px);
}
</style>
