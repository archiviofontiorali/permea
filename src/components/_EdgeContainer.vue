<script setup lang="ts">
import interact from 'interactjs'
import { getCurrentInstance, reactive, computed } from 'vue'

import type { Edge, EdgePatch, EdgeCreate, Side } from '@/stores/nodes'
import { useCanvasStore } from '@/stores/nodes'

import type { View } from './BoardCanvas.vue'
import EdgePath from './EdgePath.vue'

export interface Target {
  id?: string | null
  x: number
  y: number
  width: number
  height: number
}

export interface Handler {
  id: string | null
  from: Target
  to: Target
  side: Side | null
}

const storage = useCanvasStore()
const { edges, view } = defineProps<{ edges?: Edge[]; view: View }>()
const handle = reactive<Handler>({
  id: null,
  from: { id: null, x: 0, y: 0, width: 0, height: 0 },
  to: { id: null, x: 0, y: 0, width: 0, height: 0 },
  side: null,
})

const edgesDefault = computed(() => (edges === undefined ? storage.edges : edges))

const emit = defineEmits<{
  (e: 'drop', id: string, on: 'from' | 'to', side: Side, node: string | null): void
}>()
const hasDropEventListener = computed(() => !!getCurrentInstance()?.vnode.props?.onDrop)

interact('.edge, article.card > .handle').draggable({
  listeners: {
    start(event) {
      if (event.target.classList.contains('handle')) {
        const node = storage.getNode(event.target.parentNode.dataset.nodeId)
        handle.id = 'handle'
        handle.side = event.target.dataset.side
        Object.assign(handle.from, node)
      }
    },
    move(event) {
      const on: 'from' | 'to' = event.target.dataset.on ?? 'to'

      handle.id = event.target.dataset.edgeId ?? handle.id
      handle[on].id = 'cursor'
      handle[on].x = (event.clientX - view.x) / view.scale
      handle[on].y = (event.clientY - view.y) / view.scale

      // Needed to evaluate side when dropped
      event.target.dataset.x = event.clientX - view.x
      event.target.dataset.y = event.clientY - view.y
    },
    end() {
      handle.id = null
      handle.side = null
      handle.from.id = null
      handle.to.id = null
    },
  },
})

interact('article.card').dropzone({
  accept: '.edge, article.card > .handle',
  ondrop: function (event) {
    const node = storage.getNode(event.target.dataset.nodeId)
    const edge = event.relatedTarget.dataset.edgeId ?? handle.id

    const on: 'from' | 'to' = event.relatedTarget.dataset.on ?? 'to'
    const dx = event.relatedTarget.dataset.x - node.x
    const dy = event.relatedTarget.dataset.y - node.y

    let side: Side = dx > 0 ? 'right' : 'left'
    const [w, h] = [node.width, node.height]
    if (dy < Math.min((h / w) * dx, (-h / w) * dx)) side = 'top'
    if (dy > Math.max((h / w) * dx, (-h / w) * dx)) side = 'bottom'

    if (hasDropEventListener.value) return emit('drop', edge, on, side, node.id)

    let patch: EdgePatch = {}
    if (on === 'to') patch = { toNode: node.id, toSide: side }
    if (on === 'from') patch = { fromNode: node.id, fromSide: side }

    if (handle.id !== 'handle') return storage.updateEdge(edge, patch)

    if (handle.from.id === undefined) throw Error()
    if (handle.from.id === null) throw Error()

    patch.fromNode = handle.from.id
    patch.fromSide = handle.side ? handle.side : undefined
    return storage.createEdge(patch as EdgeCreate)
  },
})

interact(':not(article.card)').dropzone({
  accept: '.edge',
  ondrop: function (event) {
    const edge = event.relatedTarget.dataset.edgeId
    storage.deleteEdge(edge)
  },
})

function fromNode(edge: Edge): Target {
  return handle.id === edge.id && handle.from.id != null
    ? handle.from
    : storage.getNode(edge.fromNode)
}
function toNode(edge: Edge) {
  return handle.id === edge.id && handle.to.id != null ? handle.to : storage.getNode(edge.toNode)
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
  <EdgePath
    :edge="{ id: handle.id, fromSide: handle.side ? handle.side : undefined }"
    :from="handle.from"
    :to="handle.to"
    :hide="!(handle.id === 'handle' && handle.from.id !== null && handle.to.id === 'cursor')"
  />
</template>
