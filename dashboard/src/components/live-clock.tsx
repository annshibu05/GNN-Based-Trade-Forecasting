"use client"

import { useEffect, useState } from "react"

export function LiveClock() {
  const [now, setNow] = useState<Date>(() => new Date())

  useEffect(() => {
    const id = setInterval(() => setNow(new Date()), 1000)
    return () => clearInterval(id)
  }, [])

  const date = new Intl.DateTimeFormat(undefined, { dateStyle: "medium" }).format(now)
  const time = new Intl.DateTimeFormat(undefined, { timeStyle: "medium" }).format(now)

  return (
    <div
      aria-label="Current date and time"
      className="text-xs px-2 py-1 rounded-md border bg-background/70 text-muted-foreground"
    >
      <span className="sr-only">Current date:</span>
      <span>{date}</span>
      {" · "}
      <span className="sr-only">Current time:</span>
      <span>{time}</span>
    </div>
  )
}
