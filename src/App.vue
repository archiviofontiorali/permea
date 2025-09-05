<script setup lang="ts">
import CanvasBackground from './components/CanvasBackground.vue'
import CanvasItemCard from './components/CanvasItemCard.vue'

import { ref } from 'vue'
import type { Ref } from 'vue'

export interface CanvasPosition {
  x: number
  y: number
}

const canvas: Ref<CanvasPosition> = ref({ x: 0, y: 0 })

function moveCanvasView(x: number, y: number) {
  canvas.value.x = x
  canvas.value.y = y
}

function resetCanvasView() {
  moveCanvasView(0, 0)
}
</script>

<template>
  <header>
    <div class="debug relative w-full z-30 h-7">DEBUG: {{ canvas }}</div>
  </header>
  <main id="canvas">
    <header class="absolute pt-2 w-full z-20 top-7 flex justify-center">
      <button @click="resetCanvasView">Reset Origin</button>
    </header>
    <CanvasBackground :origin="canvas" @update-position="moveCanvasView" />
    <CanvasItemCard class="card absolute z-10 w-60 h-90" :origin="canvas" />
  </main>
</template>

<style scoped>
.debug {
  background-color: var(--color-purple-500);
}

button {
  background-color: var(--color-slate-700);
  border-radius: var(--radius-xl);
  padding: var(--radius-xl);
}

.card {
  background-color: var(--color-white);
}
</style>
