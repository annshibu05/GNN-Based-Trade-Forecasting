export type Prediction = {
  partner: string
  partnerCode: string // ISO3
  sector: "pharma" | "textiles"
  month: string // YYYY-MM
  value: number // USD millions
  change: number // -1..1 (delta %)
  confidence: number // 0..1
}

export type AlertItem = {
  id: string
  type: "risk" | "opportunity"
  partner: string
  partnerCode: string
  change: number
  summary: string
  title: string
  recommendations?: { partner: string; partnerCode: string; confidence: number }[]
}

export type NewsArticle = {
  id: string
  partner: string
  partnerCode: string
  title: string
  source: string
  date: string
  url: string
  sentiment: number // -1..1
  snippet: string
}

export type Explainability = {
  partnerCode: string
  attention: { partner: string; weight: number }[]
  features: { feature: string; importance: number }[]
  blurb: string
}
