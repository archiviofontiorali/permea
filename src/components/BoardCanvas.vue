<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Ref } from 'vue'

import interact from 'interactjs'
import {
  FiCrosshair,
  FiZoomIn,
  FiZoomOut,
  FiCircle,
  FiTarget,
  FiPlusCircle,
} from 'vue-icons-plus/fi'

import { BackgroundGrid as BG } from '@/constants'

import NodeContainer from './NodeContainer.vue'
import EdgeContainer from './EdgeContainer.vue'
import EdgeBuilder from './EdgeBuilder.vue'

import { useCanvasStore } from '@/stores/nodes'
import SearchPage from './SearchPage.vue'

const storage = useCanvasStore()

export interface View {
  x: number
  y: number
  scale: number
  showAxes: boolean
  showSearch: boolean
}

const view: Ref<View> = ref({ x: 0, y: 0, scale: 1.0, showAxes: true, showSearch: true })
resetView() // Execute on creation to center canvas

interact('#canvas-background').draggable({
  listeners: {
    move: (event) => {
      view.value.x += event.dx
      view.value.y += event.dy
    },
  },
})

const translateView = computed(() => ({
  transform: `translate(${view.value.x}px, ${view.value.y}px)`,
}))

const scaleTraslateView = computed(() => ({
  transform: `translate(${view.value.x}px, ${view.value.y}px) scale(${view.value.scale})`,
}))

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
    <SearchPage />

    <!-- Menu for canvas position and sizing -->
    <header class="absolute navbar navbar-bottom pb-2 z-20 gap-2 bottom-2 flex justify-center">
      <button @click="storage.demoSetup()" class="debug"><FiPlusCircle /></button>
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

      <g id="canvas-axes" :class="{ hidden: !view.showAxes }" :style="translateView">
        <circle cx="0" cy="0" r="7"></circle>
        <line x1="-40" x2="40" y1="0" y2="0" />
        <line x1="0" x2="0" y1="-40" y2="40" />
      </g>

      <g id="canvas-edges-wrapper" :style="scaleTraslateView">
        <EdgeContainer :view="view" />
        <EdgeBuilder :view="view" />
      </g>
    </svg>

    <!-- Canvas Card Nodes -->
    <section id="canvas-nodes-wrapper">
      <NodeContainer :view="view" />
    </section>
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
.navbar button.debug {
  @apply text-purple-500 border-purple-500;
}
</style>
