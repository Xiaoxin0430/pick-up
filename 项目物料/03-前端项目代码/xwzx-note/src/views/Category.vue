<template>
  <div class="category page-shell">
    <van-nav-bar
      title="笔记分类"
      left-text="返回"
      left-arrow
      fixed
      @click-left="onClickLeft"
    />

    <section class="category-hero">
      <p>把记录放进合适的小抽屉。</p>
    </section>

    <div class="category-container">
      <button
        v-for="(category, index) in displayCategories"
        :key="category.id"
        class="category-card"
        type="button"
        @click="goToCategoryNote(category.id)"
      >
        <van-icon :name="categoryIcons[index] || 'label-o'" />
        <span>{{ getCategoryTranslation(category.name, index) }}</span>
        <small>{{ categoryHints[index] || '一些轻轻放下的内容' }}</small>
      </button>
    </div>

    <tab-bar />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useNoteStore } from '../store/modules/note'
import TabBar from '../components/TabBar.vue'

const noteStore = useNoteStore()
const router = useRouter()

// const noteCategoryLabels = ['推荐', '日常', '灵感', '阅读', '观影', '随笔', '收藏']
const categoryIcons = ['like-o', 'flower-o', 'bulb-o', 'bookmark-o', 'video-o', 'edit', 'star-o']
const categoryHints = ['常翻常新的页', '生活里的细枝末节', '突然冒出的想法', '书里留下的回声', '银幕边的小记', '自由落笔', '舍不得删掉的页']

const displayCategories = computed(() => {
  return noteStore.categories
    .filter(category => category.name !== '更多')
    // .slice(0, noteCategoryLabels.length)
})

const getCategoryTranslation = (categoryName) => {
  return categoryName
}

const onClickLeft = () => {
  router.back()
}

const goToCategoryNote = (categoryId) => {
  noteStore.changeCategory(categoryId)
  router.push({
    path: '/home',
    query: { categoryId }
  })
}

onMounted(() => {
  if (!noteStore.categories.length) {
    noteStore.getCategories()
  }
})
</script>

<style scoped>
.category {
  min-height: 100vh;
  padding-top: 46px;
  padding-bottom: 78px;
}

.category-hero {
  padding: 34px 22px 12px;
}

.category-hero p {
  max-width: 15em;
  color: var(--ink-soft);
  font-size: 21px;
  line-height: 1.6;
}

.category-container {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
  padding: 14px 18px 26px;
}

.category-card {
  min-height: 138px;
  padding: 18px;
  text-align: left;
  background: rgba(255, 253, 248, 0.9);
  border: 1px solid rgba(117, 94, 70, 0.1);
  border-radius: 26px;
  box-shadow: 0 16px 36px rgba(83, 63, 42, 0.07);
}

.category-card .van-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  margin-bottom: 16px;
  color: var(--brand-deep);
  font-size: 22px;
  background: rgba(139, 111, 82, 0.1);
  border-radius: 14px;
}

.category-card span {
  display: block;
  color: var(--ink);
  font-size: 18px;
  font-weight: 700;
}

.category-card small {
  display: block;
  margin-top: 8px;
  color: var(--ink-muted);
  font-size: 12px;
  line-height: 1.5;
}
</style>
