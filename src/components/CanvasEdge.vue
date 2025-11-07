<script setup lang="ts">
import { computed } from 'vue'
import { canvas } from '@/constants'
import type { Node, Edge, canvasSide } from '@/stores/nodes'
import { useCanvasStore } from '@/stores/nodes'

const { edge } = defineProps<{ edge: Edge }>()
const storage = useCanvasStore()
const tail = storage.getNodeById(edge.fromNode)
const head = storage.getNodeById(edge.toNode)

const [ox, oy] = [canvas.edgeOffset, canvas.edgeOffset]

function vertex(node: Node, side?: canvasSide) {
  let [dx, dy] = [0, 0]
  if (side === 'top') dy -= node.height / 2
  if (side === 'left') dx -= node.width / 2
  if (side === 'right') dx += node.width / 2
  if (side === 'bottom') dy += node.height / 2
  return { x: node.x + dx, y: node.y + dy }
}

const path = computed(() => {
  const { x: tx, y: ty } = vertex(tail, edge.fromSide)
  const { x: hx, y: hy } = vertex(head, edge.toSide)
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
</script>

<template>
  <path class="edge" :d="path" />
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

<style scoped>
path.edge {
  fill: none;
  stroke: var(--color-primary);
  stroke-width: 4;
}
circle {
  fill: var(--color-primary);
}
circle.edge-head {
  stroke: var(--color-white);
  stroke-width: 4;
}
</style>
