<script setup lang="ts">
import { computed } from 'vue'
import interact from 'interactjs'

import { canvas } from '@/constants'
import type { canvasSide } from '@/stores/nodes'

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
function deltas(side?: canvasSide, offset: number = canvas.edgeOffset) {
  let [dx, dy] = [0, 0]

  if (side === 'top') dy -= offset
  if (side === 'left') dx -= offset
  if (side === 'right') dx += offset
  if (side === 'bottom') dy += offset
  return [dx, dy]
}

const tx = computed(() => sideX(from, e.fromSide))
const ty = computed(() => sideY(from, e.fromSide))

const hx = computed(() => sideX(to, e.toSide))
const hy = computed(() => sideY(to, e.toSide))

const middle = computed(() => {
  const [tdx, tdy] = deltas(e.fromSide)
  const [hdx, hdy] = deltas(e.toSide)

  let x = (tx.value + tdx + hx.value + hdx) / 2
  let y = (ty.value + tdy + hy.value + hdy) / 2

  if (e.fromSide === e.toSide) {
    if (e.fromSide === 'top') y = Math.min(ty.value + tdy, hy.value + hdy)
    if (e.fromSide === 'left') x = Math.min(tx.value + tdx, hx.value + hdx)
    if (e.fromSide === 'right') x = Math.max(tx.value + tdx, hx.value + hdx)
    if (e.fromSide === 'bottom') y = Math.max(ty.value + tdy, hy.value + hdy)
  }

  return { x: x, y: y }
})

function path(node: Node, target: { x: number; y: number }, side?: canvasSide): string {
  const [x, y] = [sideX(node, side), sideY(node, side)]
  const [dx, dy] = deltas(side)

  let path = `M${x} ${y} v${dy} h${dx}`
  if ((side === 'left' && middle.value.x > x) || (side === 'right' && middle.value.x < x)) {
    const direction = node.y > target.y ? 1 : -1
    path += `v${(node.height / 2 + canvas.edgeOffset) * direction}`
  }
  return `${path} H${target.x} V${target.y}`
}
</script>

<template>
  <circle class="edge-from" :cx="tx" :cy="ty" :r="canvas.vertexRadius" />
  <path class="edge-from" :d="path(from, middle, e.fromSide)" />
  <circle class="edge-middle" :cx="middle.x" :cy="middle.y" :r="canvas.vertexRadius" />
  <path class="edge-to" :d="path(to, middle, e.toSide)" />
  <circle class="edge-to" :cx="hx" :cy="hy" :r="canvas.vertexRadius" />
</template>

<style scoped>
path {
  fill: none;
  stroke: var(--color-primary);
  stroke-width: 4;
}
path.edge-from {
  stroke: red;
}
path.edge-to {
  stroke: blue;
}
circle {
  fill: var(--color-primary);
}
circle.edge-to {
  stroke: var(--color-white);
  stroke-width: 4;
}
</style>
