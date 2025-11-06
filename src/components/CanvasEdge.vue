<script setup lang="ts">
import { computed } from 'vue'

interface Point {
  x: number
  y: number
  end: 'arrow' | 'none'
}

const { tail, head } = defineProps<{ tail: Point; head: Point }>()

const path = computed(() => `M${tail.x} ${tail.y} L${head.x} ${head.y} Z`)
</script>

<template>
  <path class="edge" :d="path"></path>
  <circle :cx="tail.x" :cy="tail.y" :r="8" />
  <circle :cx="head.x" :cy="head.y" :r="8" />
</template>

<style scoped>
path.edge {
  fill: none;
  stroke: var(--color-primary);
  stroke-width: 4;
}
circle {
  fill: var(--color-primary);
}
</style>
