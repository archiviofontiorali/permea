<script setup lang="ts">
import { computed } from 'vue'

import { canvas } from '@/constants'
import type { Side } from '@/stores/nodes'
import type { Target } from './EdgeContainer.vue'

interface Edge {
  id: string
  fromSide?: Side
  toSide?: Side
}
interface Point {
  x: number
  y: number
}

const { edge, from, to, hide } = defineProps<{
  edge: Edge
  from: Target
  to: Target
  hide?: boolean
}>()

function sideOffset(node: { width: number; height: number }, side?: Side) {
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

const style = computed(() => ({
  opacity: hide ? 0 : 1,
}))
</script>

<template>
  <g class="edge" :data-edge-id="edge.id" data-on="from" :style="style">
    <circle :cx="tail.x" :cy="tail.y" :r="canvas.vertexRadius" />
    <path :d="path(tail, middle)" />
  </g>
  <circle :cx="middle.x" :cy="middle.y" :r="canvas.vertexRadius" :style="style" />
  <g class="edge" :data-edge-id="edge.id" data-on="to" :style="style">
    <path :d="path(head, middle)" />
    <circle :cx="head.x" :cy="head.y" :r="canvas.vertexRadius" />
  </g>
</template>

<style scoped>
path {
  fill: none;
  stroke: var(--color-primary);
  stroke-width: 4;
}
circle {
  fill: var(--color-primary);
}

.edge:hover path {
  stroke-width: 10;
}
.edge:hover circle {
  stroke: var(--color-primary);
  stroke-width: 4;
}
</style>
