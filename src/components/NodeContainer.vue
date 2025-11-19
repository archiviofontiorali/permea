<script setup lang="ts">
import { computed } from 'vue'
import interact from 'interactjs'

import { useCanvasStore } from '@/stores/nodes'
import type { Node } from '@/stores/nodes'

import type { View } from './BoardCanvas.vue'
import NodeCard from './NodeCard.vue'
import { getCurrentInstance } from 'vue'

const storage = useCanvasStore()
const { nodes, view } = defineProps<{ nodes?: Node[]; view: View }>()

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

const nodesDefault = computed(() => (nodes === undefined ? storage.nodes : nodes))
const hasMoveEventListener = computed(() => !!getCurrentInstance()?.vnode.props?.onMove)

interact('article.card > header.draggable').draggable({
  listeners: {
    move(event) {
      const id = event.target.parentNode.dataset.nodeId
      const [dx, dy] = [event.dx / view.scale, event.dy / view.scale]
      if (!hasMoveEventListener.value) storage.moveNodeRelative(id, dx, dy)
      else emit('move', id, dx, dy)
    },
  },
})
</script>

<template>
  <article
    :data-node-id="node.id"
    :key="node.id"
    class="card"
    :style="style(node)"
    v-for="node in nodesDefault"
  >
    <header class="draggable absolute w-full h-full"></header>
    <NodeCard class="relative m-4 p-4 bg-white" :node="node" />

    <header class="handle handle-row top-1" data-side="top"></header>
    <header class="handle handle-row bottom-1" data-side="bottom"></header>

    <header class="handle handle-column left-1" data-side="left"></header>
    <header class="handle handle-column right-1" data-side="right"></header>
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
  border-width: 2px;
  border-color: var(--color-primary-700);
}
article.card > header:first-child {
  background: var(--color-primary);
  color: var(--color-gray-300);
}
header.handle {
  position: absolute;
  border-radius: var(--radius-sm);
  background-color: var(--color-primary-300);
}
header.handle.handle-column {
  top: 50%;
  transform: translateY(-50%);
  width: calc(var(--spacing) * 2);
  height: calc(var(--spacing) * 8);
}
header.handle.handle-row {
  left: 50%;
  transform: translateX(-50%);

  width: calc(var(--spacing) * 8);
  height: calc(var(--spacing) * 2);
}

.center {
  transform: translate(-50%, -50%);
}
</style>
