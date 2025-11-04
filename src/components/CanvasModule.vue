<script setup lang="ts">
import { ref } from 'vue'
import type { Ref } from 'vue'

import { FiCrosshair, FiZoomIn, FiZoomOut, FiCircle, FiTarget } from 'vue-icons-plus/fi'
import interact from 'interactjs'

import { BackgroundGrid as BG } from '@/constants'
import CanvasNodeCard from './CanvasNodeCard.vue'
import CanvasDraggable from './CanvasDraggable.vue'

import { useCanvasStore } from '@/stores/nodes'

const storage = useCanvasStore()
storage.demoSetup()

export interface CanvasView {
  x: number
  y: number
  scale: number
  showAxes: boolean
}

const view: Ref<CanvasView> = ref({ x: 0, y: 0, scale: 1.0, showAxes: true })
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
    <header class="absolute navbar navbar-bottom pb-2 z-20 gap-2 bottom-2 flex justify-center">
      <button @click="zoomIn"><FiZoomIn /></button>
      <button @click="toggleAxes">
        <FiCrosshair v-if="view.showAxes" />
        <FiCircle v-else />
      </button>
      <button @click="resetView"><FiTarget /></button>
      <button @click="zoomOut"><FiZoomOut /></button>
    </header>

    <!-- Canvas Background -->
    <svg id="canvas-background" class="absolute w-full h-full bg-[#262626]">
      <pattern
        id="canvas-background-pattern"
        class="color-[#D1D1D1]"
        :x="view.x"
        :y="view.y"
        :width="BG.gap * view.scale"
        :height="BG.gap * view.scale"
        patternUnits="userSpaceOnUse"
        :patternTransform="`translate(-${BG.radius}, -${BG.radius})`"
      >
        <circle :cx="BG.radius" :cy="BG.radius" :r="BG.radius" fill="grey"></circle>
      </pattern>

      <rect width="100%" height="100%" fill="url(#canvas-background-pattern)"></rect>

      <g
        id="canvas-axes"
        :class="{ hidden: !view.showAxes }"
        :style="{ transform: `translate(${view.x}px, ${view.y}px)` }"
      >
        <circle cx="0" cy="0" r="7"></circle>
        <line x1="-40" x2="40" y1="0" y2="0" />
        <line x1="0" x2="0" y1="-40" y2="40" />
      </g>
    </svg>

    <!-- Canvas Card Nodes -->
    <CanvasDraggable
      :item="node"
      :view="view"
      :key="node.id"
      @move="storage.moveNodeRelative"
      v-for="node in storage.nodes"
    >
      <CanvasNodeCard :node="node" />
    </CanvasDraggable>
  </main>
</template>

<style scoped>
@reference "@/style.css";

svg g#canvas-axes line {
  stroke: var(--color-gray-500);
  stroke-width: 2;
}
svg g#canvas-axes circle {
  fill: var(--color-gray-500);
}

.draggable {
  position: absolute;
  background-color: var(--color-white);
}

.navbar.navbar-bottom,
.navbar.navbar-top {
  left: 50%;
  transform: translate(-50%, 0);
}

.navbar button {
  background-color: var(--color-white);
  border-radius: var(--radius-xl);
  padding: var(--radius-xl);

  @apply text-primary-700 border-2 border-primary;
}
</style>
