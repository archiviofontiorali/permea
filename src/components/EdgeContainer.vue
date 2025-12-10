<script setup lang="ts">
import interact from 'interactjs'

import { computed, reactive } from 'vue'

import { useViewStore } from '@/stores/view'
import { useStorageStore } from '@/stores/storage'
import type { Edge, EdgePatch } from '@/stores/storage'
import { side } from '@/utils'

import EdgePath from './EdgePath.vue'
import type { Target } from './EdgePath.vue'

interface Cursor {
  id: string | null
  on: 'from' | 'to'
  target: Target
}

const view = useViewStore()

const storage = useStorageStore()
const { edges: edges_ } = defineProps<{ edges?: Edge[] }>()

const cursor: Cursor = reactive({ id: null, on: 'from', target: { x: 0, y: 0 } })
const edges = computed(() => (edges_ ? edges_ : storage.edges))

function target(edge: Edge, cursor: Cursor, on: 'from' | 'to'): Target {
  if (edge.id === cursor.id && cursor.on === on) return cursor.target
  return storage.getNode(edge[`${on}Node`])
}

// NOTE: card query cannot be the same as in EdgeBuilder otherwise only one listener is preserved
const query = reactive({ edge: `.edge`, card: `.card > *` })

interact(query.edge).draggable({
  listeners: {
    start(event) {
      console.debug(`Initiate movement of edge: ${event.target.dataset.edgeId}`)
    },
    move(event) {
      // EdgePath set two data attribute: `edge-id` and `on`
      const id: string = event.target.dataset.edgeId
      const on: 'from' | 'to' = event.target.dataset.on
      const x = event.clientX - view.center.x
      const y = event.clientY - view.center.y

      // Set cursor object to actual edge, on side and cursor position
      cursor.id = id
      cursor.on = on
      cursor.target.x = x / view.scale
      cursor.target.y = y / view.scale

      // Save cursor x, y on HTML element to allow retrieving position on dropping
      event.target.dataset.x = x
      event.target.dataset.y = y
    },
    end(event) {
      console.log(`Disabling cursor from edge ${event.target.dataset.edgeId}`)
      cursor.id = null
    },
  },
})

interact(query.card).dropzone({
  accept: query.edge,
  ondrop(event) {
    // event.relatedTarget is the edge moved
    const id = event.relatedTarget.dataset.edgeId
    const on = event.relatedTarget.dataset.on

    // card dropzone are supposed to expose a node-id data attribute pointing ro existing node
    // To allow for external dropzone children must be used, so id is retrieved with parentNode
    const node = storage.getNode(event.target.parentNode.dataset.nodeId)

    console.debug(`Dropped edge ${id} over card ${node.id}`)

    const dx = event.relatedTarget.dataset.x - node.x
    const dy = event.relatedTarget.dataset.y - node.y

    let patch: EdgePatch = {}
    if (on === 'from') patch = { fromNode: node.id, fromSide: side(node, dx, dy) }
    if (on === 'to') patch = { toNode: node.id, toSide: side(node, dx, dy) }

    // TODO: missing emits when callback is set (see _EdgeContainer.vue)
    storage.updateEdge(id, patch)
  },
})
interact(`:not(${query.card})`).dropzone({
  accept: query.edge, // NOTE: accept seems to not working
  ondrop(event) {
    const id = event.relatedTarget.dataset.edgeId
    console.debug(`Dropped edge ${id} over background`)
    storage.deleteEdge(id)
  },
})
</script>

<template>
  <EdgePath
    :key="edge.id"
    :id="edge.id"
    class="edge"
    :from="target(edge, cursor, 'from')"
    :to="target(edge, cursor, 'to')"
    :from-side="edge.fromSide"
    :to-side="edge.toSide"
    :label="edge.label"
    v-for="edge in edges"
  />
</template>
<style scoped></style>
