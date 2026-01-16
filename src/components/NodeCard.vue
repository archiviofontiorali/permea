<script setup lang="ts">
import { useStorageStore, type LinkNode, type Node } from '@/stores/storage'
import { FaShareAlt, FaTrash } from 'vue-icons-plus/fa'
import { computed } from 'vue'
import { useSPARQLStore } from '@/stores/sparql'

const { node } = defineProps<{ node: Node }>()
const title = computed(() => {
  return node.metadata ? node.metadata.get('dcterms:title')?.value || node.id : node.id
})

const sparql = useSPARQLStore()
const storage = useStorageStore()

function addLink(parent: Node, uri: string, label?: string, x: number = 0, y: number = 0) {
  uri = sparql.namespace(uri)
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
          if (value.type === 'uri') {
            const other = storage.findNode(sparql.namespace(value.value))
            if (other)
              storage.createEdge({
                fromNode: node.id,
                toNode: other.id,
                label: sparql.namespace(property.value),
              })
          }
          node.metadata.set(sparql.namespace(property.value), value)
        })
      })
      .catch(console.error)
  }
}
</script>

<template>
  <main class="overflow-y-scroll" :height="`calc(${node.height} - 4rem)`">
    <header class="text-center p-3 bg-primary-700 text-primary-300">
      <h1 class="font-bold text-xl pb-1 text-nowrap overflow-x-scroll">
        <a :href="node.url" v-if="node.type === 'link'">{{ title }}</a>
        <template v-else>{{ title }}</template>
      </h1>
      <header class="flex flex-row justify-center gap-2 pt-1">
        <div class="border rounded p-1 text-xs font-bold">{{ node.type }}</div>
        <button class="border rounded p-1 active:text-white">
          <fa-trash class="w-4 h-4" @click="storage.deleteNode(node.id)" />
        </button>
      </header>
    </header>
    <main
      class="metadata p-3 grid gap-y-2 overflow-x-scroll items-center"
      style="grid-template-columns: auto auto auto"
    >
      <template :key="index" v-for="([p, v], index) of node.metadata">
        <label class="text-xs text-center py-1 px-2">{{ p }}</label>
        <p class="text-xs py-1 px-2 truncate" :title="v.value">{{ v.value }}</p>
        <p class="text-white bg-primary active:bg-primary-700 text-center h-6">
          <fa-share-alt
            @click="addLink(node, v.value, p)"
            v-if="v.type === 'uri'"
            class="h-4 my-1"
          />
        </p>
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
