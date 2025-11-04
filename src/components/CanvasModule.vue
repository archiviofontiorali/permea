<script setup lang="ts">
import { ref } from 'vue'
import type { Ref } from 'vue'

import interact from 'interactjs'

import CanvasNodeCard from './CanvasNodeCard.vue'
import CanvasDraggable from './CanvasDraggable.vue'

import { useCanvasStore } from '@/stores/nodes'

const bgCircleSize = 1

const storage = useCanvasStore()
storage.demoSetup()

export interface CanvasView {
  x: number
  y: number
  scale: number
  showAxes: boolean
}

const view: Ref<CanvasView> = ref({ x: 0, y: 0, scale: 1.0, showAxes: false })
resetView()

interact('#canvas-background').draggable({
  listeners: {
    move: (event) => {
      view.value.x += event.dx
      view.value.y += event.dy
    },
  },
})

function resetView() {
  view.value.x = window.innerWidth / 2
  view.value.y = window.innerHeight / 2
}
function toggleAxes() {
  view.value.showAxes = !view.value.showAxes
}

function zoomIn() {
  view.value.scale = Math.max(0.5, Math.min(view.value.scale * 2, 4.0))
}
function zoomOut() {
  view.value.scale = Math.max(0.5, Math.min(view.value.scale / 2, 4.0))
}
</script>

<template>
  <main id="canvas-wrapper" class="absolute overflow-hidden">
    <!-- Menu for canvas position and sizing -->
    <header class="absolute center-x pt-2 z-20 left-[50%] gap-2 top-2 flex justify-center">
      <button @click="resetView">Center Canvas</button>
      <button @click="toggleAxes">{{ view.showAxes ? 'Show' : 'Hide' }} Axes</button>
      <button @click="zoomIn">Zoom In</button>
      <button @click="zoomOut">Zoom Out</button>
    </header>

    <!-- Canvas Background -->
    <svg id="canvas-background" class="w-full h-full bg-[#262626]">
      <pattern
        id="canvas-background-pattern"
        class="color-[#D1D1D1]"
        :x="view.x"
        :y="view.y"
        :width="10 * view.scale"
        :height="10 * view.scale"
        patternUnits="userSpaceOnUse"
        :patternTransform="`translate(-${bgCircleSize}, -${bgCircleSize})`"
      >
        <circle :cx="bgCircleSize" :cy="bgCircleSize" :r="bgCircleSize" fill="grey"></circle>
      </pattern>

      <rect width="100%" height="100%" fill="url(#canvas-background-pattern)"></rect>

      <g
        id="canvas-axes"
        :class="{ hidden: view.showAxes }"
        :style="{ transform: `translate(${view.x}px, ${view.y}px)` }"
      >
        <circle cx="0" cy="0" r="10" fill="grey"></circle>
        <line x1="-50" x2="50" y1="0" y2="0" />
        <line x1="0" x2="0" y1="-50" y2="50" />
      </g>
    </svg>

    <!-- Canvas Card Nodes -->
    <CanvasDraggable
      :id="node.id"
      :x="view.x + node.x"
      :y="view.y + node.y"
      :key="node.id"
      @move="storage.moveNodeRelative"
      v-for="node in storage.nodes"
    >
      <CanvasNodeCard :node="node" />
    </CanvasDraggable>
  </main>
</template>

<style scoped>
button {
  background-color: var(--color-white);
  border-radius: var(--radius-xl);
  padding: var(--radius-xl);
}

svg g#canvas-axes line {
  stroke: var(--color-gray-500);
  stroke-width: 2;
}

.draggable {
  position: absolute;
  background-color: var(--color-white);
}

.center-x {
  transform: translate(-50%, 0);
}
</style>
