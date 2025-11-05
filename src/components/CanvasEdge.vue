<script setup lang="ts">
import { computed } from 'vue'
import type { Edge } from '@/stores/nodes'
import { useCanvasStore } from '@/stores/nodes'

// TODO: move retrieval of tail and head externally (CanvasModule)
//       define an interface for the data to pass as props like in CanavasNode
//       rename CanavasNodeCard as CanavsNode
//       to change edge path you need the other options

const storage = useCanvasStore()
const { edge } = defineProps<{ edge: Edge }>()
const tail = storage.getNodeById(edge.fromNode) || { x: 0, y: 0 }
const head = storage.getNodeById(edge.toNode) || { x: 0, y: 0 }

const path = computed(() => `M${tail.x} ${tail.y} L${head.x} ${head.y} Z`)
</script>

<template>
  <path class="edge" :d="path"></path>
</template>

<style scoped>
path.edge {
  fill: none;
  stroke: var(--color-primary);
  stroke-width: 4;
}
</style>
