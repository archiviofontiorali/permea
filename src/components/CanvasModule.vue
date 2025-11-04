<script setup lang="ts">
import { ref } from 'vue'
import type { Ref } from 'vue'

import interact from 'interactjs'

import CanvasNodeCard from './CanvasNodeCard.vue'
import CanvasDraggable from './CanvasDraggable.vue'

import { useCanvasStore } from '@/stores/nodes'

const storage = useCanvasStore()
storage.demoSetup()

export interface CanvasView {
  x: number
  y: number
  showAxes: boolean
}

const view: Ref<CanvasView> = ref({ x: 0, y: 0, showAxes: false })
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
</script>

<template>
  <main id="canvas-wrapper" class="absolute overflow-hidden">
    <!-- Menu for canvas position and sizing -->
    <header class="absolute center-x pt-2 z-20 left-[50%] gap-2 top-2 flex justify-center">
      <button @click="resetView">Center Canvas</button>
      <button @click="toggleAxes">{{ view.showAxes ? 'Show' : 'Hide' }} Axes</button>
    </header>

    <!-- Canvas Background -->
    <svg id="canvas-background" class="w-full h-full bg-[#262626]">
      <pattern
        id="canvas-background-pattern"
        class="color-[#D1D1D1]"
        :x="view.x + 10"
        :y="view.y + 10"
        width="20"
        height="20"
        patternUnits="userSpaceOnUse"
        patternTransform="translate(-0.5, -0.5)"
      >
        <circle cx="1" cy="1" r="1" fill="grey"></circle>
      </pattern>
      <rect
        width="100%"
        height="100%"
        transform="translate(10, 10)"
        fill="url(#canvas-background-pattern)"
      ></rect>

      <g
        id="canvas-axes"
        :class="{ hidden: view.showAxes }"
        :style="{ transform: `translate(${view.x}px, ${view.y}px)` }"
      >
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
