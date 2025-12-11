<script setup lang="ts">
import { computed } from 'vue'

import { canvas } from '@/constants'
import type { Side } from '@/stores/storage'

interface Point {
  x: number
  y: number
}
export interface Target extends Point {
  id?: string
  width?: number
  height?: number
}

interface EdgeProps {
  id: string
  from: Target
  to: Target
  fromSide?: Side
  toSide?: Side
  label?: string
}

const { id, from, to, fromSide, toSide, label } = defineProps<EdgeProps>()

function sideOffset(node: Target, side?: Side) {
  let [sx, sy] = [0, 0]
  if (side === 'top' && node.height) sy -= node.height / 2
  if (side === 'left' && node.width) sx -= node.width / 2
  if (side === 'right' && node.width) sx += node.width / 2
  if (side === 'bottom' && node.height) sy += node.height / 2
  return { dx: sx, dy: sy }
}

const tail = computed<Point>(() => {
  const { dx, dy } = sideOffset(from, fromSide)
  return { x: from.x + dx, y: from.y + dy }
})
const head = computed<Point>(() => {
  const { dx, dy } = sideOffset(to, toSide)
  return { x: to.x + dx, y: to.y + dy }
})

const middle = computed<Point>(() => ({
  x: (head.value.x + tail.value.x) / 2,
  y: (head.value.y + tail.value.y) / 2,
}))

function path(head: Point, tail: Point) {
  return `M${tail.x} ${tail.y} L${head.x} ${head.y}`
}

const style = computed(() => ({}))

const ch = 9.15 // 1ch in font-mono is 9.15px
const em = 16 // 1em in font-mono is 16px
</script>

<template>
  <g :class="$attrs.class" :data-edge-id="id" data-on="from" :style="style">
    <circle :cx="tail.x" :cy="tail.y" :r="canvas.vertexRadius" />
    <path :d="path(tail, middle)" />
  </g>
  <g :class="$attrs.class" :data-edge-id="id" data-on="to" :style="style">
    <path :d="path(head, middle)" />
    <circle :cx="head.x" :cy="head.y" :r="canvas.vertexRadius" />
  </g>
  <circle :cx="middle.x" :cy="middle.y" :r="canvas.vertexRadius" :style="style" v-if="!label" />
  <template v-else>
    <rect
      :x="middle.x - (label.length * ch) / 2"
      :y="middle.y - em"
      :width="label.length * ch"
      :height="2 * em"
      rx="8"
      ry="8"
    />
    <text :x="middle.x" :y="middle.y" text-anchor="middle" dominant-baseline="middle">{{
      label
    }}</text>
  </template>
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

text {
  fill: var(--color-primary-300);
}
rect {
  fill: var(--color-primary);
}

g:hover[data-on] path {
  stroke-width: 10;
}
g:hover circle {
  stroke: var(--color-primary);
  stroke-width: 4;
}
</style>
