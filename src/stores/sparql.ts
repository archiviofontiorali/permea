import { defineStore } from 'pinia'
import axios from 'axios'

export interface Query {
  property: string
  value: string
  operation: 'eq' | 'in'
}

export interface Result {
  resource: { value: string }
  property: { value: string }
  value: { value: string }
}

interface NamespaceResponse {
  'o:id': number
  'o:label': string
  'o:namespace_uri': string
  'o:prefix': string
}
interface PropertyResponse {
  property: {
    type: string
    value: string
  }

  'o:term': string
}

const endpoint = {
  omeka: { api: '/api', sparql: '/sparql' },
  fuseki: '/triplestore',
}

export const useSPARQLStore = defineStore('sparql', {
  state: () => ({
    queries: [] as Query[],
    results: [] as Result[],
    properties: new Set<string>(),
    namespaces: new Map<string, string>([
      // ['permea', 'http://localhost:8000/api/'],
      // ['rdf-syntax', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'],
      // ['rdf-schema', 'http://www.w3.org/2000/01/rdf-schema#'],
      // ['dcterms', 'http://purl.org/dc/terms/'],
      ['o', 'http://omeka.org/s/vocabs/o#'],
    ]),
  }),
  actions: {
    async query<T>(q: string) {
      const params = { params: { query: q, format: 'json' } }
      const response = await axios.get(`${endpoint.fuseki}/sparql`, params)
      console.debug(q, response)
      return response?.data?.results?.bindings as T[]
    },
    namespace(v: string): string {
      for (const [alias, ns] of this.namespaces) v = v.replace(ns, `${alias}:`)
      return v
    },

    updateNamespaces() {
      axios
        .get(`${endpoint.omeka.api}/vocabularies`)
        .then((response) => {
          response.data.forEach((o: NamespaceResponse) =>
            this.namespaces.set(o['o:prefix'], o['o:namespace_uri']),
          )
        })
        .catch((err) => console.error(err))
    },
    updateProperties() {
      const query = `SELECT DISTINCT ?property WHERE { ?resource ?property ?value . }`
      this.query<PropertyResponse>(query)
        .then((response) => {
          response
            .map((p) => this.namespace(p.property.value))
            .forEach((p) => this.properties.add(p))
        })
        .catch(console.error)
    },
    addQuery(query?: Query) {
      this.queries.push(query || { property: 'o:title', value: '', operation: 'eq' })
    },
    search(queries: Query[]) {
      let query = ''
      for (const [prefix, url] of this.namespaces) query += `\nPREFIX ${prefix}: <${url}>`

      const constraints = []
      const filters = []
      for (const q of queries) {
        if (q.operation === 'eq') constraints.push(`?resource ${q.property} "${q.value}" .`)
        if (q.operation === 'in') {
          constraints.push(`?resource ${q.property} ?value .`)
          filters.push(`FILTER CONTAINS (?value, "${q.value}") .`)
        }
      }

      query += `
      SELECT ?resource ?property ?value
      WHERE {
        ?resource ?property ?value .
        ${constraints.join('\n')}
        ${filters.join('\n')}
      }
      ORDER BY ASC($resource)`

      this.query<Result>(query)
        .then((results) => (this.results = results))
        .catch(console.error)
    },
  },
})
