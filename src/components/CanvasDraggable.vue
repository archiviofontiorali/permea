<script setup lang="ts">
import interact from 'interactjs'

const { id, x, y } = defineProps<{ id: string; x: number; y: number }>()

const emit = defineEmits<{
  (e: 'move', id: string, dx: number, dy: number): void
}>()

interact('.draggable > .drag-zone').draggable({
  listeners: {
    move(event) {
      const id = event.target.dataset.id
      emit('move', id, event.dx, event.dy)
    },
  },
})
</script>

<template>
  <div class="draggable z-10 w-60 h-90" :style="{ transform: `translate(${x}px, ${y}px)` }">
    <header class="drag-zone w-full h-6 touch-none select-none" :data-id="id" />
    <slot />
  </div>
</template>

<style scoped>
header.drag-zone {
  background-color: var(--color-slate-500);
}
</style>
