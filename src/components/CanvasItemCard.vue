<script setup lang="ts">
import type { CanvasPosition } from '../App.vue'

const { origin } = defineProps<{ origin: CanvasPosition }>()
</script>

<template>
  <article :style="{ transform: `translate(${origin.x}px, ${origin.y}px)` }">
    {{ origin }}
  </article>
</template>

<style scoped></style>
