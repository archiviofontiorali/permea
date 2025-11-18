<script setup lang="ts">
import interact from 'interactjs'
import { getCurrentInstance, reactive, computed } from 'vue'

import type { Edge, EdgePatch, canvasSide } from '@/stores/nodes'
import { useCanvasStore } from '@/stores/nodes'

import type { View } from './BoardCanvas.vue'
import EdgePath from './EdgePath.vue'

const { edges, view } = defineProps<{ edges?: Edge[]; view: View }>()
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

const edgesDefault = computed(() => (edges === undefined ? storage.edges : edges))

const emit = defineEmits<{
  (e: 'drop', id: string, on: 'head' | 'tail', side: canvasSide, node: string | null): void
}>()
const hasDropEventListener = computed(() => !!getCurrentInstance()?.vnode.props?.onDrop)

interact('.edge').draggable({
  listeners: {
    move(event) {
      cursor.id = event.target.dataset.edgeId
      cursor.on = event.target.dataset.on
      cursor.point.x = (event.clientX - view.x) / view.scale
      cursor.point.y = (event.clientY - view.y) / view.scale

      event.target.dataset.x = event.clientX - view.x
      event.target.dataset.y = event.clientY - view.y
    },
    end() {
      cursor.id = null
      cursor.on = null
    },
  },
})
interact('article.card > .handle')
  .dropzone({ accept: '.edge' })
  .on('drop', (event) => {
    const node = storage.getNode(event.target.parentNode.dataset.nodeId)
    const edge = event.relatedTarget.dataset.edgeId
    const on = event.relatedTarget.dataset.on

    const dx = event.relatedTarget.dataset.x - node.x
    const dy = event.relatedTarget.dataset.y - node.y
    const [w, h] = [node.width, node.height]

    let side: canvasSide = dx > 0 ? 'right' : 'left'
    if (dy < Math.min((h / w) * dx, (-h / w) * dx)) side = 'top'
    if (dy > Math.max((h / w) * dx, (-h / w) * dx)) side = 'bottom'

    if (hasDropEventListener.value) return emit('drop', edge, on, side, node.id)

    let patch: EdgePatch = {}
    if (on === 'head') patch = { toNode: node.id, toSide: side }
    if (on === 'tail') patch = { fromNode: node.id, fromSide: side }

    storage.updateEdge(edge, patch)
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
    v-for="edge in edgesDefault"
  />
</template>
