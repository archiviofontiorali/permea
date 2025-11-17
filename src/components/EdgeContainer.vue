<script setup lang="ts">
import interact from 'interactjs'
import { reactive } from 'vue'

import type { Edge } from '@/stores/nodes'
import { useCanvasStore } from '@/stores/nodes'

import type { View } from './BoardCanvas.vue'
import EdgePath from './EdgePath.vue'

const { edges, view } = defineProps<{ edges: Edge[]; view: View }>()
const storage = useCanvasStore()

export interface Target {
  id?: string
  x: number
  y: number
  width: number
  height: number
}

export interface Cursor {
  id: string | null
  on: 'head' | 'tail' | null
  point: Target
}
const cursor = reactive<Cursor>({ id: null, on: null, point: { x: 0, y: 0, width: 0, height: 0 } })

// const emit = defineEmits<{
//   // Drop edge side over a new node side (need dropzones)
//   (e: 'drop', id: string, on: 'head' | 'tail', side: canvasSide, node: string): void
// }>()

interact('path.edge').draggable({
  listeners: {
    move(event) {
      cursor.id = event.target.dataset.id
      cursor.on = event.target.dataset.on
      cursor.point.x = (event.clientX - view.x) / view.scale
      cursor.point.y = (event.clientY - view.y) / view.scale
    },
    end() {
      cursor.id = null
      cursor.on = null
    },
  },
})

function fromNode(edge: Edge) {
  if (cursor.id === edge.id && cursor.on === 'tail') return cursor.point
  return storage.getNode(edge.fromNode)
}
function toNode(edge: Edge) {
  if (cursor.id === edge.id && cursor.on === 'head') return cursor.point
  return storage.getNode(edge.toNode)
}
</script>

<template>
  <EdgePath
    :key="edge.id"
    :edge="edge"
    :from="fromNode(edge)"
    :to="toNode(edge)"
    v-for="edge in edges"
  />
</template>
