<script setup lang="ts">
import { useSPARQLStore, type Binding } from '@/stores/sparql'
import { useStorageStore, type LinkNode } from '@/stores/storage'
import { onMounted, reactive, ref } from 'vue'
import { FaPlusCircle, FaEye } from 'vue-icons-plus/fa'

const RECIPES = [
  ['All triples', 'SELECT ?s ?v ?o\nWHERE { ?s ?v ?o . }'],
  [
    'List items',
    `SELECT ?s ?title (COUNT(DISTINCT ?v) AS ?properties)\nWHERE {\n\t?s\t?v\t\t\t\t?o;\n\t\tdcterms:title\t?title .\n}\nGROUP BY ?title ?s`,
  ],
  ['Single item properties', `SELECT ?property ?value WHERE { permea:uri ?property ?value }`],
]

interface SearchError {
  level: 'ERROR' | 'WARNING'
  value: string
}

interface Search {
  query?: string
  results?: {
    headers: string[]
    rows: Binding[]
  }
  errors: SearchError[]
}

const sparql = useSPARQLStore()
const storage = useStorageStore()

const actualQuery = ref<string>(RECIPES[0][1])
const lastSearch: Search = reactive({ errors: [] })

/** Request data using SPARQL query */
function search(query?: string) {
  lastSearch.errors.splice(0)
  sparql
    .query(query ? query : actualQuery.value)
    .then((response) => {
      lastSearch.results = {
        headers: response.head.vars,
        rows: response.results.bindings,
      }
    })
    .catch((error) => lastSearch.errors.push({ level: 'ERROR', value: error.response.data }))
}

function addNode(uri: string) {
  uri = sparql.namespace(uri)

  if (storage.findNode(uri)) {
    lastSearch.errors.push({ level: 'ERROR', value: `Node with id: ${uri} already exists` })
    return
  }
  const node: LinkNode = {
    id: uri,
    type: 'link',
    x: 0,
    y: 0,
    width: 200,
    height: 200,
    url: uri,
  }
  storage.createNode(node)

  const query = `SELECT ?property ?value WHERE { ${uri} ?property ?value . }`
  sparql
    .query(query)
    .then((response) => {
      const node = storage.getNode(uri)
      response.results.bindings.forEach(({ property, value }) => {
        if (!node.metadata) node.metadata = new Map()
        node.metadata.set(sparql.namespace(property.value), value)
      })
    })
    .catch((error) => lastSearch.errors.push({ level: 'ERROR', value: error.response.data }))
    .finally(() => console.debug(storage.findNode(uri)))
}

function showProperties(uri: string) {
  uri = sparql.namespace(uri)
  search(`SELECT ?property ?value WHERE { ${uri} ?property ?value }`)
}

onMounted(() => {
  // sparql.updateNamespaces()
  // sparql.updateProperties()
})
</script>

<template>
  <aside :class="$attrs.class" class="bg-slate-300">
    <section id="search-form" class="p-2 grid grid-cols-3 gap-2 w-full">
      <label for="recipe">Examples: </label>
      <select name="recipe" id="recipe" class="col-span-2">
        <option
          :key="index"
          :value="name"
          v-for="([name, recipe], index) of RECIPES"
          @click="actualQuery = recipe"
        >
          {{ name }}
        </option>
      </select>

      <textarea
        name="query"
        id="query"
        v-model="actualQuery"
        class="font-mono min-h-50 col-span-3"
      />

      <button class="p-1 col-start-2" @click="search()">Search</button>
    </section>
    <hr class="my-4 border-primary" />
    <section id="search-results" class="w-full overflow-x-auto">
      <p class="border-2 border-red-800" :key="index" v-for="(e, index) of lastSearch.errors">
        {{ e }}
      </p>
      <table class="table-auto" v-if="lastSearch.results">
        <thead>
          <th :key="h" v-for="h in lastSearch.results.headers">{{ h }}</th>
        </thead>
        <tbody>
          <tr :key="i" v-for="(row, i) in lastSearch.results.rows" class="_w-full">
            <td :key="j" v-for="(b, j) in row" class="px-2 text-nowrap whitespace-nowrap">
              <template v-if="b.type === 'uri'">
                <fa-plus-circle class="inline pr-2" @click="addNode(b.value)" />
                <fa-eye class="inline pr-2" @click="showProperties(b.value)" />

                <a class="link text-nowrap overflow-x-auto max-w-[45ch]" :href="b.value">
                  {{ sparql.namespace(b.value) }}
                </a>
              </template>

              <template v-else>{{ b.value }}</template>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </aside>
</template>

<style scoped>
@reference "@/style.css";

button,
textarea,
select,
label {
  padding: 0.5rem;
  outline: 2px solid var(--color-primary-700);
  border-radius: 0.5rem;
}
label {
  font-weight: bold;
  background-color: var(--color-primary-700);
  color: var(--color-primary-300);
}
button:active {
  background-color: var(--color-primary-700);
  color: var(--color-primary-300);
}
td > svg {
  color: var(--color-primary);
}
td > svg:active {
  color: var(--color-primary-700);
}
</style>
