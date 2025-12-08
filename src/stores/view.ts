import { defineStore } from 'pinia'

export const useViewStore = defineStore('view', {
  state: () => ({ center: { x: 0, y: 0 }, scale: 1.0, axes: true }),
  // getters: {},
  actions: {
    reset() {
      this.center.x = window.innerWidth / 2
      this.center.y = window.innerHeight / 2
      this.scale = 1
    },
    zoomIn() {
      this.scale = Math.max(0.5, Math.min(this.scale * 2, 4.0))
    },
    zoomOut() {
      this.scale = Math.max(0.5, Math.min(this.scale / 2, 4.0))
    },
  },
})
