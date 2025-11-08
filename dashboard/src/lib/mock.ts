import type { AlertItem, Explainability, NewsArticle, Prediction } from "./types"

type Params = { sector: "pharma" | "textiles"; month: string; partner?: string }

const partners = [
  ["United States", "USA"],
  ["Germany", "DEU"],
  ["United Arab Emirates", "ARE"],
  ["China", "CHN"],
  ["Australia", "AUS"],
  ["United Kingdom", "GBR"],
  ["Japan", "JPN"],
  ["Brazil", "BRA"],
] as const

export function mockPredictions({ sector, month }: Params): Prediction[] {
  return partners.map(([name, code], i) => {
    const base = sector === "pharma" ? 1200 : 900
    const jitter = (i % 5) * 80 + (sector === "pharma" ? 50 : 0)
    const value = Math.max(150, base + jitter - (code === "CHN" ? 200 : 0))
    const change = (Math.sin(i * 1.3 + (sector === "pharma" ? 0.2 : 0.6)) - (code === "DEU" ? 0.4 : 0)) * 0.12
    const confidence = Math.min(0.95, 0.7 + (i % 3) * 0.08)
    return { partner: name, partnerCode: code, sector, month, value, change, confidence }
  })
}

export function mockAlerts({ sector }: Params): AlertItem[] {
  const preds = mockPredictions({ sector, month: new Date().toISOString().slice(0, 7) })
  return preds
    .filter((p) => Math.abs(p.change) > 0.06)
    .slice(0, 6)
    .map((p, idx) => {
      const type = p.change >= 0 ? "opportunity" : "risk"
      return {
        id: `${type}-${idx}`,
        type,
        partner: p.partner,
        partnerCode: p.partnerCode,
        change: p.change,
        title: type === "opportunity" ? `Growth in ${p.partner}` : `Risk in ${p.partner}`,
        summary:
          type === "opportunity"
            ? `Prediction increased due to improving sentiment and demand signals.`
            : `Prediction dropped due to negative news and supply risk.`,
        recommendations:
          type === "risk"
            ? [
                { partner: "United States", partnerCode: "USA", confidence: 0.86 },
                { partner: "United Arab Emirates", partnerCode: "ARE", confidence: 0.78 },
              ]
            : undefined,
      } satisfies AlertItem
    })
}

export function mockNews({ partner }: Params): NewsArticle[] {
  const code = partner || "USA"
  return [
    {
      id: `${code}-1`,
      partner: "Partner",
      partnerCode: code,
      title: "Policy shift sparks demand uptick in pharma imports",
      source: "GlobalTrade Daily",
      date: new Date().toISOString(),
      url: "https://example.com/article-1",
      sentiment: 0.42,
      snippet: "Analysts point to policy clarity and easing logistics as key drivers...",
    },
    {
      id: `${code}-2`,
      partner: "Partner",
      partnerCode: code,
      title: "Supply disruption risk from port congestion",
      source: "Maritime Wire",
      date: new Date().toISOString(),
      url: "https://example.com/article-2",
      sentiment: -0.31,
      snippet: "Industry groups warn of congestion at major transshipment hubs...",
    },
  ]
}

export function mockExplainability({ partner }: Params): Explainability {
  const neighbors = [
    { partner: "USA", weight: 0.42 },
    { partner: "ARE", weight: 0.21 },
    { partner: "DEU", weight: 0.18 },
    { partner: "GBR", weight: 0.14 },
  ]
  const features = [
    { feature: "News Sentiment", importance: 0.36 },
    { feature: "GDP Growth", importance: 0.22 },
    { feature: "Historical Exports", importance: 0.18 },
    { feature: "FX Rate", importance: 0.14 },
    { feature: "Logistics Index", importance: 0.1 },
  ]
  return {
    partnerCode: partner || "USA",
    attention: neighbors,
    features,
    blurb:
      "Prediction reflects positive sector news and strong demand signals, tempered by FX volatility. Attention focuses on USA and ARE as influential neighbors in the trade graph.",
  }
}
