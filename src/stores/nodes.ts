import { sample } from 'underscore'
import { defineStore } from 'pinia'
import { DemoConfig } from '@/constants'

/** The canvasColor type is used to encode color data for nodes and edges. Colors attributes expect a string. Colors can be specified in hex format e.g. "#FF0000", or using one of the preset colors,  */
export type canvasColor = string
export type canvasSide = 'top' | 'right' | 'bottom' | 'left'
export type canvasEnd = 'arrow' | 'none'

// For specifics about implementation go to https://jsoncanvas.org/spec/1.0/
export interface GenericNode {
  id: string
  type: 'text' | 'file' | 'link' | 'group'
  x: number
  y: number
  width: number
  height: number
  color?: canvasColor
}

export interface TextNode extends GenericNode {
  type: 'text'
  text: string
}
export interface LinkNode extends GenericNode {
  type: 'link'
  url: string
}
// export interface FileNode extends Node { file: string, subpath?: string }
// export interface GroupNode extends Node { ... }

export type Node = TextNode | LinkNode

// For specifics about implementation go to https://jsoncanvas.org/spec/1.0/
export interface Edge {
  id: string

  /** is the node id where the connection starts. */
  fromNode: string
  fromSide?: canvasSide
  fromEnd?: canvasEnd // default: none

  /** is the node id where the connection ends. */
  toNode: string
  toSide?: canvasSide
  toEnd?: canvasEnd // default: arrow

  color?: canvasColor
  label?: string
}

export const useCanvasStore = defineStore('canvas', {
  state: () => {
    return {
      nodes: [] as Node[],
      edges: [] as Edge[],
    }
  },
  getters: {},
  actions: {
    getNodeById(id: string): Node {
      const result = this.nodes.find((item) => item.id === id)
      if (result === undefined) throw Error()
      return result
    },
    top: (node: Node): number => node.y - node.height / 2,
    bottom: (node: Node): number => node.y + node.height / 2,
    left: (node: Node): number => node.x - node.width / 2,
    right: (node: Node): number => node.x + node.width / 2,
    asMap() {
      this.nodes.reduce((acc, item) => ({ ...acc, [item.id]: item }), {})
    },
    demoSetup() {
      const nNodes = this.nodes.length
      for (let i = 0; i < DemoConfig.nodes; i++) {
        const node: Node = {
          id: `card-${nNodes + i}`,
          type: 'text',
          x: Math.floor((2 * Math.random() - 1) * DemoConfig.offset),
          y: Math.floor((2 * Math.random() - 1) * DemoConfig.offset),
          width: DemoConfig.nodeWidth,
          height: DemoConfig.nodeHeight,
          text: 'Hello World',
        }
        if (nNodes + i > 0)
          this.edges.push({
            id: `edge-${nNodes + i}`,
            fromNode: (sample(this.nodes) || node).id,
            toNode: node.id,
            fromSide: sample<canvasSide[]>(['top', 'bottom', 'left', 'right']),
            toSide: sample<canvasSide[]>(['top', 'bottom', 'left', 'right']),
          })
        this.nodes.push(node)
      }
    },
    moveNode(id: string, x: number, y: number) {
      const node = this.getNodeById(id)
      if (node === undefined) throw Error()

      node.x = x
      node.y = y
    },
    moveNodeRelative(id: string, dx: number = 0, dy: number = 0) {
      const node = this.getNodeById(id)
      if (node === undefined) throw Error()
      node.x += dx
      node.y += dy
    },
  },
})
