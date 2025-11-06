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


const path = computed(() => `M${tail.x} ${tail.y} L${head.x} ${head.y} Z`)
</script>

<template>
  <path class="edge" :d="path" />
  <circle
    :cx="vertex(tail, edge.fromSide).x"
    :cy="vertex(tail, edge.fromSide).y"
    :r="canvas.vertexRadius"
  />
  <circle
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
</style>
