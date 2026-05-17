import type { Metadata } from "next"
import "@/styles/globals.css"

export const metadata: Metadata = {
  title: "SHL Assessment Recommender",
  description: "AI-powered assessment recommendations with an elegant green-white interface",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">
        {children}
      </body>
    </html>
  )
}
