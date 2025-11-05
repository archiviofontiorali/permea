<script setup lang="ts">
import { computed } from 'vue'

import interact from 'interactjs'
import { FiMoreHorizontal } from 'vue-icons-plus/fi'

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

interact('.draggable > .drag').draggable({
  listeners: {
    move(event) {
      const id = event.target.parentNode.dataset.id
      emit('move', id, event.dx / view.scale, event.dy / view.scale)
    },
  },
})
</script>

<template>
  <div class="draggable z-10 bg-white border-4 border-primary" :data-id="item.id" :style="style">
    <div class="drag text-gray-300 bg-primary h-4 flex flex-row justify-around items-center">
      <FiMoreHorizontal />
      <FiMoreHorizontal />
    </div>
    <slot />
  </div>
</template>

<style scoped>
@reference "@/style.css";

.draggable {
  position: absolute;
  transform-origin: 0 0;
  @apply touch-none select-none;
}
</style>
