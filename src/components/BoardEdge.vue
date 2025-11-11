<script setup lang="ts">
import { computed } from 'vue'
import interact from 'interactjs'

import { canvas } from '@/constants'
import type { canvasSide, Edge } from '@/stores/nodes'

import type { Node } from './BoardDraggable.vue'

export interface Edge {
  id: string
  fromSide?: canvasSide
  toSide?: canvasSide
}

const { edge: e, from, to } = defineProps<{ edge: Edge; from: Node; to: Node }>()

function sideX(node: Node, side?: canvasSide): number {
  if (side === 'left') return node.x - node.width / 2
  if (side === 'right') return node.x + node.width / 2
  return node.x
}
function sideY(node: Node, side?: canvasSide): number {
  if (side === 'top') return node.y - node.height / 2
  if (side === 'bottom') return node.y + node.height / 2
  return node.y
}
const tail = computed(() => ({ x: sideX(from, e.fromSide), y: sideY(from, e.fromSide) }))
const head = computed(() => ({ x: sideX(to, e.toSide), y: sideY(to, e.toSide) }))

const middle = computed(() => {
  let x = (head.value.x + tail.value.x) / 2
  let y = (head.value.y + tail.value.y) / 2

  if (e.fromSide === e.toSide) {
    if (e.fromSide === 'top') y = Math.min(tail.value.y, head.value.y) - canvas.edgeOffset
    if (e.fromSide === 'left') x = Math.min(tail.value.x, head.value.x) - canvas.edgeOffset
    if (e.fromSide === 'right') x = Math.max(tail.value.x, head.value.x) + canvas.edgeOffset
    if (e.fromSide === 'bottom') y = Math.max(tail.value.y, head.value.y) + canvas.edgeOffset
  }

  if (e.fromSide === 'right') x = Math.max(x, tail.value.x + canvas.edgeOffset)
  if (e.toSide === 'right') x = Math.max(x, head.value.x + canvas.edgeOffset)

  if (e.fromSide === 'left') x = Math.min(x, tail.value.x - canvas.edgeOffset)
  if (e.toSide === 'left') x = Math.min(x, head.value.x - canvas.edgeOffset)

  return { x: x, y: y }
})

function deltas(side?: canvasSide, offset: number = canvas.edgeOffset) {
  let [dx, dy] = [0, 0]

  if (side === 'top') dy -= offset
  if (side === 'left') dx -= offset
  if (side === 'right') dx += offset
  if (side === 'bottom') dy += offset
  return [dx, dy]
}

const fromPath = computed(() => {
  // const [s, o] = [e.fromSide, canvas.edgeOffset]
  const [tx, ty] = [tail.value.x, tail.value.y]
  const [mx, my] = [middle.value.x, middle.value.y]
  const [dx, dy] = deltas(e.fromSide)

  return `M${tx} ${ty} h${dx} v${dy} H${mx} V${my}`
})
const toPath = computed(() => {
  const [hx, hy] = [head.value.x, head.value.y]
  const [mx, my] = [middle.value.x, middle.value.y]
  const [dx, dy] = deltas(e.toSide)

  return `M${hx} ${hy} h${dx} v${dy} H${mx} V${my}`
})
</script>

<template>
  <circle class="edge-from" :cx="tail.x" :cy="tail.y" :r="canvas.vertexRadius" />
  <path class="edge-from" :d="fromPath" />
  <circle class="edge-middle" :cx="middle.x" :cy="middle.y" :r="canvas.vertexRadius" />
  <path class="edge-to" :d="toPath" />
  <circle class="edge-to" :cx="head.x" :cy="head.y" :r="canvas.vertexRadius" />
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
circle.edge-to {
  stroke: var(--color-white);
  stroke-width: 4;
}
</style>
