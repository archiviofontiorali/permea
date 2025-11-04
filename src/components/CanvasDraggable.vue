<script setup lang="ts">
import { computed } from 'vue'
import interact from 'interactjs'
import type { CanvasView } from './CanvasModule.vue'

export interface Draggable {
  id: string
  x: number
  y: number
  width: number
  height: number
}

const { item, view } = defineProps<{ item: Draggable; view: CanvasView }>()
const style = computed(() => ({
  width: `${item.width}px`,
  height: `${item.height}px`,
  transform: `
    translate(${view.x}px, ${view.y}px)
    scale(${view.scale})
    translate(${item.x - item.width / 2}px, ${item.y - item.height / 2}px)
  `,
}))

const emit = defineEmits<{
  (e: 'move', id: string, dx: number, dy: number): void
}>()

interact('.draggable > .drag-zone').draggable({
  listeners: {
    move(event) {
      const id = event.target.dataset.id
      emit('move', id, event.dx / view.scale, event.dy / view.scale)
    },
  },
})
</script>

<template>
  <div class="draggable absolute z-10 border-4 border-gray-500" :style="style">
    <header class="drag-zone w-full h-6 touch-none select-none" :data-id="item.id" />
    <slot />
  </div>
</template>

<style scoped>
header.drag-zone {
  background-color: var(--color-slate-500);
}
.draggable {
  transform-origin: 0 0;
}
</style>
