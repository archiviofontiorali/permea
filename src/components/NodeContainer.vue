<script setup lang="ts">
import interact from 'interactjs'
import { FiMoreHorizontal } from 'vue-icons-plus/fi'

import type { View } from './BoardCanvas.vue'
import NodeCard from './NodeCard.vue'

import type { Node } from '@/stores/nodes'

const { nodes, view } = defineProps<{ nodes: Node[]; view: View }>()

const emit = defineEmits<{
  (e: 'move', id: string, dx: number, dy: number): void
}>()

function style(node: Node) {
  return {
    zIndex: 10,
    width: `${node.width}px`,
    height: `${node.height}px`,
    transform: `
      translate(${view.x}px, ${view.y}px)
      scale(${view.scale})
      translate(${node.x - node.width / 2}px, ${node.y - node.height / 2}px)
    `,
  }
}

interact('article.card > header.draggable').draggable({
  listeners: {
    move(event) {
      const id = event.target.parentNode.id
      emit('move', id, event.dx / view.scale, event.dy / view.scale)
    },
  },
})
</script>

<template>
  <article
    :id="node.id"
    :key="node.id"
    class="card border-4"
    :style="style(node)"
    v-for="node in nodes"
  >
    <header class="draggable flex flex-row justify-around align-middle">
      <FiMoreHorizontal />
      <FiMoreHorizontal />
    </header>
    <NodeCard :node="node" />
  </article>
</template>

<style scoped>
@reference "@/style.css";

article.card {
  position: absolute;
  transform-origin: 0 0;
  @apply touch-none select-none;
}

article.card {
  background: var(--color-white);
  border-color: var(--color-primary);
}
article.card > header {
  background: var(--color-primary);
  color: var(--color-gray-300);
}
</style>
