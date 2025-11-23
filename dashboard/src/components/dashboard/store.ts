// // "use client"

// // import { create } from "zustand"
// // import type { AlertItem, Explainability, NewsArticle, Prediction } from "@/lib/types"
// // import { mockAlerts, mockExplainability, mockNews, mockPredictions } from "@/lib/mock"

// // type State = {
// //   sector: "pharma" | "textiles"
// //   month: string // YYYY-MM
// //   selectedPartner?: string
// //   predictions: Prediction[]
// //   alerts: AlertItem[]
// //   news: NewsArticle[]
// //   explainability?: Explainability
// // }

// // type Actions = {
// //   setSector: (s: "pharma" | "textiles") => void
// //   setMonth: (m: string) => void
// //   selectPartner: (countryCode: string) => void
// //   // Simulated loading hooks
// //   loadPredictions: () => Promise<void>
// //   loadAlerts: () => Promise<void>
// //   loadNews: (partner?: string) => Promise<void>
// //   loadExplainability: (partner?: string) => Promise<void>
// // }

// // export const useDashboardStore = create<State & Actions>((set, get) => ({
// //   sector: "pharma",
// //   month: new Date().toISOString().slice(0, 7),
// //   predictions: [],
// //   alerts: [],
// //   news: [],
// //   explainability: undefined,

// //   setSector: (sector) => set({ sector }),
// //   setMonth: (month) => set({ month }),
// //   selectPartner: (selectedPartner) => set({ selectedPartner }),

// //   loadPredictions: async () => {
// //     const { sector, month } = get()
// //     // TODO: Integrate with backend endpoint `/api/predictions?sector={sector}&month={month}`
// //     // const predictions = await fetch(`/api/predictions?sector=${sector}&month=${month}`).then(r => r.json())
// //     const predictions = mockPredictions({ sector, month })
// //     set({ predictions })
// //   },

// //   loadAlerts: async () => {
// //     const { sector, month } = get()
// //     // TODO: Integrate with backend endpoint `/api/alerts?sector={sector}&month={month}`
// //     const alerts = mockAlerts({ sector, month })
// //     set({ alerts })
// //   },

// //   loadNews: async (partner) => {
// //     const { sector, month } = get()
// //     // TODO: Integrate with backend endpoint `/api/news?sector={sector}&month={month}&partner=${partner||""}`
// //     const news = mockNews({ sector, month, partner })
// //     set({ news })
// //   },

// //   loadExplainability: async (partner) => {
// //     const { sector, month } = get()
// //     // TODO: Integrate with backend endpoint `/api/explainability?sector={sector}&month={month}&partner=${partner||""}`
// //     const explainability = mockExplainability({ sector, month, partner })
// //     set({ explainability })
// //   },
// // }))



// "use client"
// import { create } from "zustand"
// import type { AlertItem, Explainability, NewsArticle, Prediction } from "@/lib/types"

// type State = {
//   sector: "pharma" | "textiles"
//   month: string
//   selectedPartner?: string
//   predictions: Prediction[]
//   alerts: AlertItem[]
//   news: NewsArticle[]
//   explainability?: Explainability
// }

// type Actions = {
//   setSector: (s: "pharma" | "textiles") => void
//   setMonth: (m: string) => void
//   selectPartner: (countryCode: string) => void
//   loadPredictions: () => Promise<void>
//   loadAlerts: () => Promise<void>
//   loadNews: (partner?: string) => Promise<void>
//   loadExplainability: (partner?: string) => Promise<void>
// }

// const API_URL = "http://localhost:8000"

// export const useDashboardStore = create<State & Actions>((set, get) => ({
//   sector: "pharma",
//   month: new Date().toISOString().slice(0, 7),
//   predictions: [],
//   alerts: [],
//   news: [],
//   explainability: undefined,

//   setSector: (sector) => set({ sector }),
//   setMonth: (month) => set({ month }),
//   selectPartner: (selectedPartner) => set({ selectedPartner }),

//   loadPredictions: async () => {
//     const { sector, month } = get()
//     const res = await fetch(`${API_URL}/predictions?sector=${sector}&month=${month}`)
//     const predictions = await res.json()
//     set({ predictions })
//   },

//   loadAlerts: async () => {
//     const { sector, month } = get()
//     const res = await fetch(`${API_URL}/alerts?sector=${sector}&month=${month}`)
//     const alerts = await res.json()
//     set({ alerts })
//   },

//   loadNews: async (partner) => {
//     const { sector, month } = get()
//     const res = await fetch(`${API_URL}/news?sector=${sector}&month=${month}&partner=${partner}`)
//     const news = await res.json()
//     set({ news })
//   },

//   loadExplainability: async (partner) => {
//     const { sector, month } = get()
//     const res = await fetch(`${API_URL}/explainability?sector=${sector}&month=${month}&partner=${partner}`)
//     const explainability = await res.json()
//     set({ explainability })
//   },
// }))




"use client"

import { create } from "zustand"
import type { AlertItem, Explainability, NewsArticle, Prediction } from "@/lib/types"

// Type definitions for reference (ensure these match in your lib/types.ts):
// interface Prediction {
//   partnerCode: string  // ISO3 code for React key
//   partner: string      // Country name
//   value: number
//   change: number       // Decimal format (0.125 = 12.5%)
//   confidence: "high" | "medium" | "low"
//   risk_level: "low" | "medium" | "high"
// }
//
// interface NewsArticle {
//   id: string
//   title: string
//   snippet: string      // Note: 'snippet' not 'summary'
//   source: string
//   url: string
//   date: string         // Note: 'date' not 'published_at'
//   sentiment: number    // Note: number not string (-1.0 to 1.0)
//   relevance_score: number
//   country_code?: string
// }

// Backend API base URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

type State = {
  sector: "pharma" | "textiles"
  month: string // YYYY-MM
  selectedPartner?: string
  predictions: Prediction[]
  alerts: AlertItem[]
  news: NewsArticle[]
  explainability?: Explainability
  loading: {
    predictions: boolean
    alerts: boolean
    news: boolean
    explainability: boolean
  }
  error: {
    predictions?: string
    alerts?: string
    news?: string
    explainability?: string
  }
}

type Actions = {
  setSector: (s: "pharma" | "textiles") => void
  setMonth: (m: string) => void
  selectPartner: (countryCode: string) => void
  loadPredictions: () => Promise<void>
  loadAlerts: () => Promise<void>
  loadNews: (partner?: string) => Promise<void>
  loadExplainability: (partner?: string) => Promise<void>
}

export const useDashboardStore = create<State & Actions>((set, get) => ({
  sector: "pharma",
  month: new Date().toISOString().slice(0, 7),
  predictions: [],
  alerts: [],
  news: [],
  explainability: undefined,
  loading: {
    predictions: false,
    alerts: false,
    news: false,
    explainability: false,
  },
  error: {},

  setSector: (sector) => set({ sector }),
  setMonth: (month) => set({ month }),
  selectPartner: (selectedPartner) => set({ selectedPartner }),

  loadPredictions: async () => {
    const { sector, month } = get()
    
    set((state) => ({
      loading: { ...state.loading, predictions: true },
      error: { ...state.error, predictions: undefined },
    }))

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/predictions?sector=${sector}&month=${month}`
      )
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const predictions = await response.json()
      
      set((state) => ({
        predictions,
        loading: { ...state.loading, predictions: false },
      }))
    } catch (error) {
      console.error("Failed to load predictions:", error)
      set((state) => ({
        loading: { ...state.loading, predictions: false },
        error: {
          ...state.error,
          predictions: error instanceof Error ? error.message : "Failed to load predictions",
        },
      }))
    }
  },

  loadAlerts: async () => {
    const { sector, month } = get()
    
    set((state) => ({
      loading: { ...state.loading, alerts: true },
      error: { ...state.error, alerts: undefined },
    }))

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/alerts?sector=${sector}&month=${month}`
      )
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const alerts = await response.json()
      
      set((state) => ({
        alerts,
        loading: { ...state.loading, alerts: false },
      }))
    } catch (error) {
      console.error("Failed to load alerts:", error)
      set((state) => ({
        loading: { ...state.loading, alerts: false },
        error: {
          ...state.error,
          alerts: error instanceof Error ? error.message : "Failed to load alerts",
        },
      }))
    }
  },

  loadNews: async (partner) => {
    const { sector, month } = get()
    
    set((state) => ({
      loading: { ...state.loading, news: true },
      error: { ...state.error, news: undefined },
    }))

    try {
      const params = new URLSearchParams({
        sector,
        month,
      })
      
      if (partner) {
        params.append("partner", partner)
      }
      
      const response = await fetch(
        `${API_BASE_URL}/api/news?${params.toString()}`
      )
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const news = await response.json()
      
      set((state) => ({
        news,
        loading: { ...state.loading, news: false },
      }))
    } catch (error) {
      console.error("Failed to load news:", error)
      set((state) => ({
        loading: { ...state.loading, news: false },
        error: {
          ...state.error,
          news: error instanceof Error ? error.message : "Failed to load news",
        },
      }))
    }
  },

  loadExplainability: async (partner) => {
    const { sector, month, selectedPartner } = get()
    const targetPartner = partner || selectedPartner
    
    if (!targetPartner) {
      console.warn("No partner selected for explainability")
      return
    }
    if (!targetPartner || targetPartner === "undefined") {
      set({ explainability: undefined })
      return
    }
    set((state) => ({
      loading: { ...state.loading, explainability: true },
      error: { ...state.error, explainability: undefined },
    }))

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/explainability?sector=${sector}&month=${month}&partner=${targetPartner}`
      )
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const explainability = await response.json()
      
      set((state) => ({
        explainability,
        loading: { ...state.loading, explainability: false },
      }))
    } catch (error) {
      console.error("Failed to load explainability:", error)
      set((state) => ({
        loading: { ...state.loading, explainability: false },
        error: {
          ...state.error,
          explainability: error instanceof Error ? error.message : "Failed to load explainability",
        },
      }))
    }
  },
}))