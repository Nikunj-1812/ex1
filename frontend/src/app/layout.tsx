import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'MAI-PAEP - Multi-AI Prompt Intelligence Platform',
  description: 'Compare responses from multiple AI models with advanced ML evaluation and accuracy scoring',
  keywords: 'AI, Machine Learning, GPT, Claude, Gemini, LLaMA, Prompt Engineering, Evaluation',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className={inter.className}>
        {children}
      </body>
    </html>
  )
}
