<script setup lang="ts">
import { computed } from 'vue'
import interact from 'interactjs'

import { canvas } from '@/constants'
import type { canvasSide, Edge } from '@/stores/nodes'
import { useCanvasStore } from '@/stores/nodes'
import type { View } from './BoardCanvas.vue'

export interface Extremity {
  x: number
  y: number
  width: number
  height: number
}
export interface Move {
  x: number
  y: number
  on: 'from' | 'to' | 'head' | 'tail'
}

const { edge, view, move } = defineProps<{ edge: Edge; view: View; move?: Move }>()
const storage = useCanvasStore()

const tail = storage.getNodeById(edge.fromNode)
const head = storage.getNodeById(edge.toNode)

const [ox, oy] = [canvas.edgeOffset, canvas.edgeOffset]

function vertex(node: Extremity, side?: canvasSide) {
  let [dx, dy] = [0, 0]
  if (side === 'top') dy -= node.height / 2
  if (side === 'left') dx -= node.width / 2
  if (side === 'right') dx += node.width / 2
  if (side === 'bottom') dy += node.height / 2
  return { x: node.x + dx, y: node.y + dy }
}

const path = computed(() => {
  const tail = storage.getNodeById(edge.fromNode)
  const head = storage.getNodeById(edge.toNode)

  const { x: tx, y: ty } =
    move && ['tail', 'from'].includes(move.on) ? move : vertex(tail, edge.fromSide)
  const { x: hx, y: hy } =
    move && ['head', 'to'].includes(move.on) ? move : vertex(head, edge.toSide)

  const [ts, hs] = [edge.fromSide, edge.toSide]
  const [mx, my] = [(tail.x + head.x) / 2, (tail.y + head.y) / 2]
  const s = `M${tx} ${ty}`
  const e = `L${hx} ${hy}`

  let p = ''

  if (ts === 'top') {
    if (hs === 'top') p = `V${Math.min(ty, hy) - oy} H${hx}`
    if (hs === 'left') p = `V${Math.min(hx - ox > tx ? hy : my, ty - oy)} H${hx - ox} V${hy}`
    if (hs === 'right') p = `V${Math.max(hx + ox < tx ? hy : my, ty + oy)} H${hx + ox} V${hy}`
    if (hs === 'bottom')
      p = `V${Math.min(ty - oy, my)}` + (hy > ty ? `H${mx} V${hy + oy}` : ``) + `H${hx}`
  }

  if (ts === 'bottom') {
    if (hs === 'top')
      p = `V${Math.max(ty + oy, my)}` + (hy < ty ? `H${mx} V${hy - oy}` : ``) + `H${hx}`
    if (hs === 'left') p = `V${Math.max(hx - ox > tx ? hy : my, ty + oy)} H${hx - ox} V${hy}`
    if (hs === 'right') p = `V${Math.min(hx + ox < tx ? hy : my + oy, ty + oy)} H${hx + ox} V${hy}`
    if (hs === 'bottom') p = `V${Math.max(ty, hy) + oy} H${hx}`
  }

  if (ts === 'left') {
    if (hs === 'top') p = `H${Math.min(hy - oy > ty ? hx : mx, tx - ox)} V${hy - oy} H${hx}`
    if (hs === 'left') p = `H${Math.min(tx, hx) - ox} V${hy}`
    if (hs === 'right')
      p = `H${Math.min(tx - ox, mx)}` + (hx > tx ? `V${my} H${hx + ox}` : ``) + `V${hy}`
    if (hs === 'bottom') p = `H${Math.min(hy + oy < ty ? hx : mx, tx - ox)} V${hy + oy} H${hx}`
  }

  if (ts === 'right') {
    if (hs === 'top') p = `H${Math.max(hy - oy > ty ? hx : mx, tx + ox)} V${hy - oy} H${hx}`
    if (hs === 'left')
      p = `H${Math.max(tx + ox, mx)}` + (hx < tx ? `V${my} H${hx - ox}` : ``) + `V${hy}`
    if (hs === 'right') p = `H${Math.max(tx, hx) + ox} V${hy}`
    if (hs === 'bottom') p = `H${Math.max(hy + oy < ty ? hx : mx, tx + ox)} V${hy + oy} H${hx}`
  }

  return `${s} ${p} ${e}`
})

const emit = defineEmits<{
  (e: 'move', id: string, x: number, y: number): void
  (e: 'update', id: string, patch: { fromNode?: string; toNode?: string }): void
  (e: 'remove', id: string): void
}>()

interact('path.edge').draggable({
  listeners: {
    move(event) {
      emit('move', event.target.id, event.clientX - view.x, event.clientY - view.y)
    },
    end(event) {
      const target = event.target.dataset.target
      if (target) {
        // storage.updateEdge(event.target.id, { fromNode: target })
        emit('update', event.target.id, { fromNode: target })
      } else {
        // storage.removeEdge(event.target.id)
        emit('remove', event.target.id)
      }

      emit('move', '', 0, 0)
    },
  },
})
interact('.draggable')
  .dropzone({})
  .on('dragenter', function (event) {
    event.relatedTarget.dataset.target = event.target.dataset.id
  })
  .on('dragleave', function (event) {
    delete event.relatedTarget.dataset.target
  })
</script>

<template>
  <path :id="edge.id" :edge-from="edge.fromNode" :edge-to="edge.toNode" class="edge" :d="path" />
  <circle
    class="edge-tail"
    :cx="vertex(tail, edge.fromSide).x"
    :cy="vertex(tail, edge.fromSide).y"
    :r="canvas.vertexRadius"
  />
  <circle
    class="edge-head"
    :cx="vertex(head, edge.toSide).x"
    :cy="vertex(head, edge.toSide).y"
    :r="canvas.vertexRadius"
  />
</template>
