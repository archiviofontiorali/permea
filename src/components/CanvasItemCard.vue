<script setup lang="ts">
import type { CanvasPosition } from '../App.vue'
import { ref } from 'vue'
import type { Ref } from 'vue'
import interact from 'interactjs'

const { origin } = defineProps<{ origin: CanvasPosition }>()

const position: Ref<CanvasPosition> = ref({ x: 0, y: 0 })

interact('#card .drag-zone').draggable({
  listeners: {
    move(event) {
      position.value.x += event.dx
      position.value.y += event.dy
    },
  },
})
</script>

<template>
  <article
    id="card"
    class="flex flex-col justify-between align-middle text-center"
    :style="{ transform: `translate(${origin.x + position.x}px, ${origin.y + position.y}px)` }"
  >
    <div class="w-full h-5 bg-blue-500 drag-zone"></div>
    {{ origin }}<br />
    {{ position }}
  </article>
</template>

<style scoped></style>
