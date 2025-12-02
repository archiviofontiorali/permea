<script setup lang="ts">
import { hostname } from 'os'
import SparqlClient from 'sparql-http-client'
import { reactive, onMounted } from 'vue'

const endpoint_ = 'http://localhost:8000'
const endpoint = 'http://localhost:8080'
const query = `
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?resource ?property ?value
WHERE {
    ?resource dcterms:title ?title .
    ?resource ?property ?value .
}
ORDER BY ASC(?resource)
LIMIT 10
`

console.log(query)

const client = new SparqlClient({
  endpointUrl: `${endpoint}/sparql`,
  headers: {},
})

interface Result {
  resource: { value: string }
  property: { value: string }
  value: { value: string }
}

const resources = reactive<Result[]>([])

onMounted(() => {
  const stream = client.query.select(query)

  stream.on('data', (result) => {
    resources.push(result)
  })
  stream.on('error', (err) => {
    console.error(err)
  })
})

function ns(value: string): string {
  return value
    .replace(`${endpoint_}/api/`, 'permea:')
    .replace('http://www.w3.org/1999/02/22-rdf-syntax-ns#', 'rdf-syntax:')
    .replace('http://www.w3.org/2000/01/rdf-schema#', 'rdf-schema:')
    .replace('http://purl.org/dc/terms/', 'dcterms:')
    .replace('http://omeka.org/s/vocabs/o#', 'omeka:')
}
</script>

<template>
  <p :key="key" v-for="[key, r] of resources.entries()">
    {{ ns(r.resource.value) }} - {{ ns(r.property.value) }} - {{ ns(r.value.value) }}
  </p>
</template>
