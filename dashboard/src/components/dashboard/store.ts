"use client"

import { create } from "zustand"
import type { AlertItem, Explainability, NewsArticle, Prediction } from "@/lib/types"
import { mockAlerts, mockExplainability, mockNews, mockPredictions } from "@/lib/mock"

type State = {
  sector: "pharma" | "textiles"
  month: string // YYYY-MM
  selectedPartner?: string
  predictions: Prediction[]
  alerts: AlertItem[]
  news: NewsArticle[]
  explainability?: Explainability
}

type Actions = {
  setSector: (s: "pharma" | "textiles") => void
  setMonth: (m: string) => void
  selectPartner: (countryCode: string) => void
  // Simulated loading hooks
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

  setSector: (sector) => set({ sector }),
  setMonth: (month) => set({ month }),
  selectPartner: (selectedPartner) => set({ selectedPartner }),

  loadPredictions: async () => {
    const { sector, month } = get()
    // TODO: Integrate with backend endpoint `/api/predictions?sector={sector}&month={month}`
    // const predictions = await fetch(`/api/predictions?sector=${sector}&month=${month}`).then(r => r.json())
    const predictions = mockPredictions({ sector, month })
    set({ predictions })
  },

  loadAlerts: async () => {
    const { sector, month } = get()
    // TODO: Integrate with backend endpoint `/api/alerts?sector={sector}&month={month}`
    const alerts = mockAlerts({ sector, month })
    set({ alerts })
  },

  loadNews: async (partner) => {
    const { sector, month } = get()
    // TODO: Integrate with backend endpoint `/api/news?sector={sector}&month={month}&partner=${partner||""}`
    const news = mockNews({ sector, month, partner })
    set({ news })
  },

  loadExplainability: async (partner) => {
    const { sector, month } = get()
    // TODO: Integrate with backend endpoint `/api/explainability?sector={sector}&month={month}&partner=${partner||""}`
    const explainability = mockExplainability({ sector, month, partner })
    set({ explainability })
  },
}))
