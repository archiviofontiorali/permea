<script setup lang="ts">
import interact from 'interactjs'
import type { CanvasView } from './CanvasModule.vue'

const { view } = defineProps<{ view: CanvasView }>()

const emit = defineEmits<{
  (e: 'move-view', dx: number, dy: number): void
}>()

interact('#canvas-background').draggable({
  listeners: {
    move: (event) => emit('move-view', event.dx, event.dy),
  },
})
</script>

<template>
  <svg id="canvas-background" class="absolute w-full h-full bg-[#262626]">
    <pattern
      id="canvas-background-pattern"
      class="color-[#D1D1D1]"
      :x="view.x"
      :y="view.y"
      width="20"
      height="20"
      patternUnits="userSpaceOnUse"
      patternTransform="translate(-0.5, -0.5)"
    >
      <circle cx="0.7" cy="0.7" r="0.7" fill="white"></circle>
    </pattern>
    <rect
      width="100%"
      height="100%"
      transform="translate(10, 10)"
      fill="url(#canvas-background-pattern)"
    ></rect>
  </svg>
</template>
