<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Ref } from 'vue'

import CanvasBackground from './CanvasBackground.vue'
import CanvasItemCard from './CanvasItemCard.vue'
import CanvasDraggable from './CanvasDraggable.vue'

export interface CanvasView {
  x: number // x position of the actual canvas view
  y: number // y position of the actual canvas view
}

const view: Ref<CanvasView> = ref({ x: 0, y: 0 })
function resetView() {
  view.value.x = 0
  view.value.y = 0
}
function moveView(dx: number, dy: number) {
  view.value.x += dx
  view.value.y += dy
}

export interface LODItem {
  id: string
  title: string
}

export interface CardItem {
  id: string
  item: LODItem
  x: number
  y: number
}

const nodes: Ref<CardItem[]> = ref([
  { id: 'card-1', item: { id: 'item-1', title: 'First Item' }, x: 0, y: 0 },
  { id: 'card-2', item: { id: 'item-2', title: 'Second Item' }, x: 200, y: 30 },
  { id: 'card-3', item: { id: 'item-3', title: 'Third Item' }, x: 600, y: 50 },
])
// convert a list in a map with id as key
const cache = computed(() =>
  nodes.value.reduce((accumulator, item) => ({ ...accumulator, [item.id]: item }), {}),
)

function moveNode(id: string, dx: number, dy: number) {
  cache.value[id].x += dx
  cache.value[id].y += dy
}
</script>

<template>
  <!-- Menu for canvas position and sizing -->
  <header class="center-x absolute pt-2 z-20 left-[50%] top-2 flex justify-center">
    <button @click="resetView">Center Canvas</button>
  </header>

  <!-- Canvas Background -->
  <CanvasBackground :view="view" @move-view="moveView" />

  <!-- Canvas Card Nodes -->
  <CanvasDraggable
    :reference="node.id"
    :x="view.x + node.x"
    :y="view.y + node.y"
    :key="node.id"
    @move-card="moveNode"
    v-for="node in nodes"
  >
    <CanvasItemCard :item="node.item" />
  </CanvasDraggable>
</template>

<style scoped>
button {
  background-color: var(--color-white);
  border-radius: var(--radius-xl);
  padding: var(--radius-xl);
}

.draggable {
  position: absolute;
  background-color: var(--color-white);
}

.center-x {
  transform: translate(-50%, 0);
}
</style>
