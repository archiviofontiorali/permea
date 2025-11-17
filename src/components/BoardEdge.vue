<script setup lang="ts">
import { computed } from 'vue'
import interact from 'interactjs'

import { canvas } from '@/constants'
import type { View, Cursor } from './BoardCanvas.vue'
import type { Edge } from '@/stores/nodes'
import { useCanvasStore } from '@/stores/nodes'

interface Point {
  x: number
  y: number
}

import type { canvasSide } from '@/stores/nodes'

function sideOffset(node: { width: number; height: number }, side?: canvasSide) {
  let [sx, sy] = [0, 0]
  if (side === 'top') sy -= node.height / 2
  if (side === 'left') sx -= node.width / 2
  if (side === 'right') sx += node.width / 2
  if (side === 'bottom') sy += node.height / 2
  return { dx: sx, dy: sy }
}

const storage = useCanvasStore()

const { edge, view, cursor } = defineProps<{ edge: Edge; view: View; cursor?: Cursor }>()

const tail = computed<Point>(() => {
  if (cursor && cursor.on === 'tail') return { x: cursor.x, y: cursor.y }
  const node = storage.getNode(edge.fromNode)
  const { dx, dy } = sideOffset(node, edge.fromSide)
  return { x: node.x + dx, y: node.y + dy }
})
const head = computed<Point>(() => {
  if (cursor && cursor.on === 'head') return { x: cursor.x, y: cursor.y }
  const node = storage.getNode(edge.toNode)
  const { dx, dy } = sideOffset(node, edge.fromSide)
  return { x: node.x + dx, y: node.y + dy }
})

const middle = computed(() => ({
  x: (head.value.x + tail.value.x) / 2,
  y: (head.value.y + tail.value.y) / 2,
}))

function path(head: Point, tail: Point) {
  return `M${tail.x} ${tail.y} L${head.x} ${head.y}`
}

const emit = defineEmits<{
  (e: 'move', id: string, on: 'head' | 'tail', x: number, y: number): void
  (e: 'drop', id: string): void
}>()

interact('path.edge').draggable({
  listeners: {
    move(event) {
      emit(
        'move',
        event.target.dataset.id,
        event.target.dataset.on,
        event.clientX - view.x,
        event.clientY - view.y,
      )
    },
    end(event) {
      emit('drop', event.target.dataset.id)
    },
  },
})
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
