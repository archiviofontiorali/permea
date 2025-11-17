<script setup lang="ts">
import { computed } from 'vue'

import { canvas } from '@/constants'
import type { Edge, canvasSide } from '@/stores/nodes'
import type { Target } from './EdgeContainer.vue'

interface Point {
  x: number
  y: number
}

const { edge, from, to } = defineProps<{ edge: Edge; from: Target; to: Target }>()

function sideOffset(node: { width: number; height: number }, side?: canvasSide) {
  let [sx, sy] = [0, 0]
  if (side === 'top') sy -= node.height / 2
  if (side === 'left') sx -= node.width / 2
  if (side === 'right') sx += node.width / 2
  if (side === 'bottom') sy += node.height / 2
  return { dx: sx, dy: sy }
}

const tail = computed<Point>(() => {
  const { dx, dy } = sideOffset(from, edge.fromSide)
  return { x: from.x + dx, y: from.y + dy }
})
const head = computed<Point>(() => {
  const { dx, dy } = sideOffset(to, edge.toSide)
  return { x: to.x + dx, y: to.y + dy }
})

const middle = computed<Point>(() => ({
  x: (head.value.x + tail.value.x) / 2,
  y: (head.value.y + tail.value.y) / 2,
}))

function path(head: Point, tail: Point) {
  return `M${tail.x} ${tail.y} L${head.x} ${head.y}`
}
</script>

<template>
  <path class="edge" :data-id="edge.id" data-on="tail" :d="path(tail, middle)" />
  <path class="edge" :data-id="edge.id" data-on="head" :d="path(head, middle)" />
  <circle class="edge-tail" :cx="tail.x" :cy="tail.y" :r="canvas.vertexRadius" />
  <circle class="edge-middle" :cx="middle.x" :cy="middle.y" :r="canvas.vertexRadius" />
  <circle class="edge-head" :cx="head.x" :cy="head.y" :r="canvas.vertexRadius" />
</template>

<style scoped>
path {
  fill: none;
  stroke: var(--color-primary);
  stroke-width: 4;
}
path:hover {
  stroke-width: 10;
}
circle {
  fill: var(--color-primary);
}
circle.edge-to {
  stroke: var(--color-white);
  stroke-width: 4;
}
</style>
