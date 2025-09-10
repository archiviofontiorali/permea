<script setup lang="ts">
import interact from 'interactjs'
import type { CardItem } from './CanvasModule.vue'

const { node } = defineProps<{ node: CardItem }>()
const emit = defineEmits<{
  (e: 'move-card', id: string, dx: number, dy: number)
}>()

interact('.draggable .drag-zone').draggable({
  listeners: {
    move(event) {
      const id = event.target.dataset.id
      emit('move-card', id, event.dx, event.dy)
    },
  },
})
</script>

<template>
  <header class="drag-zone w-full touch-none select-none" :data-id="node.id">
    {{ node.item.title }}
  </header>
</template>

<style scoped>
header.drag-zone {
  background-color: var(--color-blue-500);
}
</style>
