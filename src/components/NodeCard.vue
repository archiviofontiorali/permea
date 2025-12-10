<script setup lang="ts">
import { useStorageStore, type LinkNode, type Node } from '@/stores/storage'
import { FaDotCircle } from 'vue-icons-plus/fa'
import { computed } from 'vue'
import { useSPARQLStore } from '@/stores/sparql'

const { node } = defineProps<{ node: Node }>()
const title = computed(() => {
  return node.metadata ? node.metadata.get('dcterms:title')?.value || node.id : node.id
})

const sparql = useSPARQLStore()
const storage = useStorageStore()

function addLink(parent: Node, uri: string, label?: string, x: number = 0, y: number = 0) {
  if (storage.findNode(uri)) {
    console.warn({ level: 'WARNING', value: `Node with id: ${uri} already exists` })
    return
  }
  const node: LinkNode = { id: uri, type: 'link', x: x, y: y, width: 400, height: 400, url: uri }
  storage.createNode(node)

  storage.createEdge({ fromNode: parent.id, toNode: node.id, label: label })

  if (uri.startsWith('permea')) {
    sparql
      .query(`SELECT ?property ?value WHERE { ${uri} ?property ?value . }`)
      .then((response) => {
        const node = storage.getNode(uri)
        response.results.bindings.forEach(({ property, value }) => {
          if (!node.metadata) node.metadata = new Map()
          node.metadata.set(sparql.namespace(property.value), value)
        })
      })
      .catch(console.error)
  }
}
</script>

<template>
  <main class="overflow-y-scroll" :height="`calc(${node.height} - 4rem)`">
    <header class="text-center p-2 mb-2 bg-primary-700 text-primary-300">
      <p class="text-xs text-left">{{ node.type }}</p>
      <h1 class="font-bold text-xl">{{ title }}</h1>
    </header>
    <main
      class="metadata p-1 grid gap-y-2 overflow-x-scroll items-center"
      style="grid-template-columns: auto auto auto"
    >
      <template :key="index" v-for="([p, v], index) of node.metadata">
        <span class="text-primary active:text-primary-700 align-center pr-1">
          <fa-dot-circle class="" v-if="v.type === 'uri'" @click="addLink(node, v.value, p)" />
        </span>
        <label class="text-xs text-center py-1 px-2">{{ p }}</label>
        <p class="text-xs py-1 px-2 truncate" :title="v.value">{{ v.value }}</p>
      </template>
    </main>
  </main>
</template>

<style scoped>
.metadata > label {
  color: var(--color-primary-300);
  background: var(--color-primary-700);
  outline: var(--color-primary-700) 1px solid;
}

.metadata > p {
  outline: var(--color-primary-700) 1px solid;
}
</style>
