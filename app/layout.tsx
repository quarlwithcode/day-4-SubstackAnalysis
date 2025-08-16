import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Neuropsych Brand Analyzer',
  description: 'Analyze the neuropsychology behind influencer brands through their language',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <nav className="border-b border-notion-border">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <a href="/" className="text-xl font-semibold">
                  Neuropsych Analyzer
                </a>
              </div>
              <div className="flex items-center space-x-6">
                <a href="/influencers" className="text-notion-text-secondary hover:text-notion-text">
                  Influencers
                </a>
                <a href="/about" className="text-notion-text-secondary hover:text-notion-text">
                  About
                </a>
              </div>
            </div>
          </div>
        </nav>
        {children}
      </body>
    </html>
  )
}