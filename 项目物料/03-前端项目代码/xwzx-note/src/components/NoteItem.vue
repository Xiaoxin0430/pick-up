<template>
  <article class="note-card" @click="goToDetail">
    <div class="note-copy">
      <div class="note-kicker">
        <span class="note-tag">{{ noteTag }}</span>
        <span class="note-dot"></span>
        <span>{{ noteTime }}</span>
      </div>

      <h3 class="note-title">{{ note.title }}</h3>
      <p class="note-desc">{{ note.description || '还没有摘要，点开看看这页记录里写了什么。' }}</p>

      <div class="note-footer">
        <span>{{ note.views || 0 }} 次翻阅</span>
        <van-icon name="arrow" />
      </div>
    </div>

    <div class="note-image" v-if="note.image">
      <img :src="note.image" :alt="`笔记配图：${note.title}`">
    </div>
  </article>
</template>

<script setup>
import { computed, defineProps } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  note: {
    type: Object,
    required: true
  }
})

const router = useRouter()

const noteTag = computed(() => props.note.author || '未分类')
const noteTime = computed(() => props.note.publishTime || props.note.publishedTime || props.note.publish_time || '刚刚更新')

const goToDetail = () => {
  router.push(`/note/detail/${props.note.id}`)
}
</script>

<style scoped>
.note-card {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 112px;
  gap: 16px;
  margin: 0 18px 16px;
  padding: 18px;
  overflow: hidden;
  cursor: pointer;
  background:
    linear-gradient(135deg, rgba(255, 253, 248, 0.98), rgba(250, 242, 230, 0.92));
  border: 1px solid rgba(117, 94, 70, 0.1);
  border-radius: 26px;
  box-shadow: 0 16px 42px rgba(83, 63, 42, 0.08);
  animation: page-rise 0.45s ease both;
}

.note-card::before {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    linear-gradient(90deg, rgba(139, 111, 82, 0.05) 1px, transparent 1px),
    linear-gradient(rgba(139, 111, 82, 0.035) 1px, transparent 1px);
  background-size: 22px 22px;
  mask-image: linear-gradient(90deg, transparent, #000 16%, #000 80%, transparent);
}

.note-copy {
  position: relative;
  z-index: 1;
  min-width: 0;
}

.note-kicker {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  color: var(--ink-muted);
  font-size: 12px;
  letter-spacing: 0.03em;
}

.note-tag {
  max-width: 7em;
  padding: 3px 9px;
  overflow: hidden;
  color: var(--brand-deep);
  text-overflow: ellipsis;
  white-space: nowrap;
  background: rgba(139, 111, 82, 0.1);
  border-radius: 999px;
}

.note-dot {
  width: 4px;
  height: 4px;
  background: rgba(139, 111, 82, 0.36);
  border-radius: 50%;
}

.note-title {
  display: -webkit-box;
  margin: 0 0 10px;
  overflow: hidden;
  color: var(--ink);
  font-size: 18px;
  font-weight: 700;
  line-height: 1.42;
  letter-spacing: 0.01em;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  line-clamp: 2;
}

.note-desc {
  display: -webkit-box;
  min-height: 40px;
  margin: 0;
  overflow: hidden;
  color: var(--ink-soft);
  font-size: 14px;
  line-height: 1.7;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  line-clamp: 2;
}

.note-footer {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 16px;
  color: var(--ink-muted);
  font-size: 12px;
}

.note-image {
  position: relative;
  z-index: 1;
  width: 112px;
  height: 132px;
  overflow: hidden;
  border-radius: 22px;
  background: var(--paper-warm);
  box-shadow: inset 0 0 0 1px rgba(117, 94, 70, 0.08);
}

.note-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: saturate(0.86) contrast(0.96);
}

@media (max-width: 390px) {
  .note-card {
    grid-template-columns: minmax(0, 1fr) 94px;
    gap: 12px;
    padding: 16px;
  }

  .note-image {
    width: 94px;
    height: 118px;
  }
}
</style>
