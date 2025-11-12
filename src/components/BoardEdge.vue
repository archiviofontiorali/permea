<script setup lang="ts">
import { computed } from 'vue'
import { canvas } from '@/constants'
import type { Cursor } from './BoardCanvas.vue'
import type { Edge } from '@/stores/nodes'
import { useCanvasStore } from '@/stores/nodes'

interface Point {
  x: number
  y: number
}

// import type { canvasSide } from '@/stores/nodes'

// function sideX(node: Node, side?: canvasSide): number {
//   if (side === 'left') return node.x - node.width / 2
//   if (side === 'right') return node.x + node.width / 2
//   return node.x
// }
// function sideY(node: Node, side?: canvasSide): number {
//   if (side === 'top') return node.y - node.height / 2
//   if (side === 'bottom') return node.y + node.height / 2
//   return node.y
// }
// function deltas(side?: canvasSide, offset: number = canvas.edgeOffset) {
//   let [dx, dy] = [0, 0]

//   if (side === 'top') dy -= offset
//   if (side === 'left') dx -= offset
//   if (side === 'right') dx += offset
//   if (side === 'bottom') dy += offset
//   return [dx, dy]
// }

const storage = useCanvasStore()

const { edge, cursor } = defineProps<{ edge: Edge; cursor?: Cursor }>()

const tail = computed<Point>(() => {
  if (cursor && cursor.on === 'tail') return { x: cursor.x, y: cursor.y }
  const node = storage.getNode(edge.fromNode)
  return { x: node.x, y: node.y }
})
const head = computed<Point>(() => {
  if (cursor && cursor.on === 'head') return { x: cursor.x, y: cursor.y }
  const node = storage.getNode(edge.toNode)
  return { x: node.x, y: node.y }
})

const middle = computed(() => ({
  x: (head.value.x + tail.value.x) / 2,
  y: (head.value.y + tail.value.y) / 2,
}))

function path(head: Point, tail: Point) {
  return `M${tail.x} ${tail.y} L${head.x} ${head.y}`
}

const emit = defineEmits<{
  (e: 'drag', id: string, on: 'head' | 'tail'): void
}>()
</script>

<template>
  <path
    ref="tail"
    class="edge"
    :d="path(tail, middle)"
    @mousedown="emit('drag', edge.id, 'tail')"
  />
  <path
    ref="head"
    class="edge"
    :d="path(head, middle)"
    @mousedown="emit('drag', edge.id, 'head')"
  />
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
