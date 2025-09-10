<script setup lang="ts">
import interact from 'interactjs'

const { reference, x, y } = defineProps<{ reference: string; x: number; y: number }>()
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
  <div class="draggable z-10 w-60 h-90" :style="{ transform: `translate(${x}px, ${y}px)` }">
    <header class="drag-zone w-full h-6 touch-none select-none" :data-id="reference" />
    <slot />
  </div>
</template>

<style scoped>
header.drag-zone {
  background-color: var(--color-blue-500);
}
</style>
