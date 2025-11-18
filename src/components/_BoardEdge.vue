<script setup lang="ts">
import { computed } from 'vue'

import { canvas } from '@/constants'
import type { Side } from '@/stores/nodes'

export interface Edge {
  id: string
  fromSide?: Side
  toSide?: Side
}
export interface Node {
  x: number
  y: number
  width: number
  height: number
}
function deltas(side?: Side, offset: number = canvas.edgeOffset) {
  let [dx, dy] = [0, 0]

  if (side === 'top') dy -= offset
  if (side === 'left') dx -= offset
  if (side === 'right') dx += offset
  if (side === 'bottom') dy += offset
  return [dx, dy]
}
const { edge, from, to } = defineProps<{ edge: Edge; from: Node; to: Node }>()

const tx = computed(() => sideX(from, edge.fromSide))
const ty = computed(() => sideY(from, edge.fromSide))

const hx = computed(() => sideX(to, edge.toSide))
const hy = computed(() => sideY(to, edge.toSide))

const middle = computed(() => {
  const [tdx, tdy] = deltas(edge.fromSide)
  const [hdx, hdy] = deltas(edge.toSide)

  let x = (tx.value + tdx + hx.value + hdx) / 2
  let y = (ty.value + tdy + hy.value + hdy) / 2

  if (edge.fromSide === edge.toSide) {
    if (edge.fromSide === 'top') y = Math.min(ty.value + tdy, hy.value + hdy)
    if (edge.fromSide === 'left') x = Math.min(tx.value + tdx, hx.value + hdx)
    if (edge.fromSide === 'right') x = Math.max(tx.value + tdx, hx.value + hdx)
    if (edge.fromSide === 'bottom') y = Math.max(ty.value + tdy, hy.value + hdy)
  }

  return { x: x, y: y }
})

function path(node: Node, target: { x: number; y: number }, side?: Side): string {
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
  <path class="edge-from" :d="path(from, middle, edge.fromSide)" />
  <circle class="edge-middle" :cx="middle.x" :cy="middle.y" :r="canvas.vertexRadius" />
  <path class="edge-to" :d="path(to, middle, edge.toSide)" />
  <circle class="edge-to" :cx="hx" :cy="hy" :r="canvas.vertexRadius" />
</template>
