import { defineStore } from 'pinia'

export const useViewStore = defineStore('view', {
  state: () => ({ debug: true }),
  // getters: {},
  // actions: {},
})
