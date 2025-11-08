"use client"

import { useEffect, useState } from "react"

export function ThemeToggle() {
  const [isDark, setIsDark] = useState(false)

  useEffect(() => {
    const root = document.documentElement
    const stored = localStorage.getItem("theme")
    const prefers = window.matchMedia("(prefers-color-scheme: dark)").matches
    const nextDark = stored ? stored === "dark" : prefers
    setIsDark(nextDark)
    root.classList.toggle("dark", nextDark)
  }, [])

  function toggle() {
    const root = document.documentElement
    const next = !isDark
    setIsDark(next)
    root.classList.toggle("dark", next)
    localStorage.setItem("theme", next ? "dark" : "light")
  }

  return (
    <button
      onClick={toggle}
      aria-pressed={isDark}
      aria-label="Toggle theme"
      className="inline-flex items-center gap-2 rounded-md border px-3 py-2 text-sm hover:bg-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
      title={isDark ? "Switch to light" : "Switch to dark"}
    >
      <span className="size-2.5 rounded-full" style={{ background: "var(--color-chart-1)" }} />
      {isDark ? "Dark" : "Light"}
    </button>
  )
}
