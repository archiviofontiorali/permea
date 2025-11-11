<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Ref } from 'vue'

import {
  FiCrosshair,
  FiZoomIn,
  FiZoomOut,
  FiCircle,
  FiTarget,
  FiPlusCircle,
} from 'vue-icons-plus/fi'
import interact from 'interactjs'

import BoardDraggable from './BoardDraggable.vue'
import type {} from './BoardDraggable.vue'

import { BackgroundGrid as BG } from '@/constants'
import BoardNode from './BoardNode.vue'

import BoardEdge from './BoardEdge.vue'

import { useCanvasStore } from '@/stores/nodes'
import type {} from '@/stores/nodes'

const storage = useCanvasStore()

export interface View {
  x: number
  y: number
  scale: number
  showAxes: boolean
}

const view: Ref<View> = ref({ x: 0, y: 0, scale: 1.0, showAxes: true })
resetView()

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

// const movingEdge: {
//   id?: string
//   move?: { x: number; y: number; on: 'from' }
// } = reactive({})

// function onMovingEdge(id: string, x: number, y: number) {
//   movingEdge.id = id
//   movingEdge.move = { x: x, y: y, on: 'from' }
// }
</script>

<template>
  <main id="canvas-wrapper" class="absolute overflow-hidden">
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
        <BoardEdge
          :key="edge.id"
          :edge="edge"
          :from="storage.getNodeById(edge.fromNode)"
          :to="storage.getNodeById(edge.toNode)"
          v-for="edge in storage.edges"
        />
      </g>
    </svg>

    <!-- Canvas Card Nodes -->
    <section id="canvas-nodes-wrapper">
      <BoardDraggable
        :key="node.id"
        :item="node"
        :view="view"
        @move="storage.moveNodeRelative"
        v-for="node in storage.nodes"
      >
        <BoardNode :node="node" />
      </BoardDraggable>
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
