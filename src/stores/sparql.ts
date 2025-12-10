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

export interface Value {
  type: 'uri' | 'literal'
  value: string
}
export interface Binding {
  [key: string]: Value
}

interface Response {
  head: { vars: string[] }
  results: {
    bindings: Binding[]
  }
}

const endpoint = {
  omeka: {
    api: 'https://permea.afor.dev/omeka/api',
    sparql: '/sparql',
  },
  fuseki: 'https://permea.afor.dev/triplestore',
}

export const useSPARQLStore = defineStore('sparql', {
  state: () => ({
    queries: [] as Query[],
    results: [] as Result[],
    properties: new Set<string>(),
    namespaces: new Map<string, string>([
      ['permea-items', `${endpoint.omeka.api}/items/`],
      ['permea', `${endpoint.omeka.api}/`],
      ['foaf', 'http://xmlns.com/foaf/0.1/'],
      ['schema', 'https://schema.org/'],
      ['rdf-syntax', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'],
      ['rdf-schema', 'http://www.w3.org/2000/01/rdf-schema#'],
      ['dcterms', 'http://purl.org/dc/terms/'],
      ['o', 'http://omeka.org/s/vocabs/o#'],
    ]),
  }),
  actions: {
    async query(q: string): Promise<Response> {
      let preamble = ''
      this.namespaces.forEach((url, prefix) => (preamble += `PREFIX ${prefix}: <${url}>\n`))

      const params = { params: { query: `${preamble}${q}`, format: 'json' } }
      const response = await axios.get<Response>(`${endpoint.fuseki}/sparql`, params)

      console.debug(params.params.query, response)
      return response?.data
    },
    namespace(v: string): string {
      for (const [alias, uri] of this.namespaces) v = v.replace(uri, `${alias}:`)
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
      this.query(query)
        .then((response) => {
          response.results.bindings
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
