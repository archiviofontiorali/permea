<script setup lang="ts">
import interact from 'interactjs'
import { getCurrentInstance, reactive, computed } from 'vue'

import type { Target } from './EdgePath.vue'
import type { Node, Edge, EdgePatch, EdgeCreate, Side } from '@/stores/nodes'
import EdgePath from './EdgePath.vue'
import type { View } from './BoardCanvas.vue'
import { useCanvasStore } from '@/stores/nodes'
import { side } from '@/utils'

interface Cursor {
  from: Node | null
  to: Target | null

  side?: Side
}

const storage = useCanvasStore()

const { view } = defineProps<{ view: View }>()

const cursor = reactive<Cursor>({ from: null, to: null })
const query = reactive({ card: `.card > header`, handle: `.card > header.handle` })
// NOTE: card query cannot be the same as in EdgeContainer otherwise only one listener is preserved

interact(query.handle).draggable({
  listeners: {
    start(event) {
      // Node card is assumed to expose node id and side over handle
      const node = storage.getNode(event.target.parentNode.dataset.nodeId)
      const side = event.target.dataset.side

      console.log(`Creating new edge from node: ${node.id}`)

      cursor.from = node
      cursor.side = side
    },
    move(event) {
      const x = event.clientX - view.x
      const y = event.clientY - view.y

      cursor.to = { x: x / view.scale, y: y / view.scale }

      // Save cursor x, y on HTML element to allow retrieving position on dropping
      event.target.dataset.x = x
      event.target.dataset.y = y
    },
    end(event) {
      console.debug(`Ending creation of edge from node ${event.target.parentNode.dataset.nodeId}`)
      cursor.from = null
      cursor.to = null
      cursor.side = undefined
    },
  },
})

interact(query.card).dropzone({
  accept: query.handle, // NOTE: accept seems to not working
  ondrop(event) {
    if (!cursor.from) return console.error(`cursor.from invalid. Value: ${cursor.from}`)

    const node = storage.getNode(event.target.parentNode.dataset.nodeId)

    console.debug(`Dropped cursor from node ${cursor.from.id} over card ${node.id}`)

    const dx = event.relatedTarget.dataset.x - node.x
    const dy = event.relatedTarget.dataset.y - node.y
    const toSide = side(node, dx, dy)

    const edge: EdgeCreate = {
      fromNode: cursor.from.id,
      fromSide: cursor.side,
      toNode: node.id,
      toSide: toSide,
    }

    // TODO: missing emits when callback is set (see _EdgeContainer.vue)
    storage.createEdge(edge)
  },
})
</script>

<template>
  <EdgePath
    id="cursor"
    class="cursor"
    :from="cursor.from"
    :to="cursor.to"
    :from-side="cursor.side"
    v-if="cursor.from && cursor.to"
  />
</template>
<style></style>
