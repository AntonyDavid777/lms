import { Analytics } from '@vercel/analytics/next'
import type { Metadata, Viewport } from 'next'
import { AuthProvider } from '@/contexts/auth-context'
import './globals.css'

export const metadata: Metadata = {
  title: 'TechTots LMS - Learn, Grow, Excel',
  description:
    'An innovative Learning Management System designed for tech education. Explore courses, track your progress, and join a community of learners.',
  generator: 'v0.app',
  keywords:
    'Learning Management System, Online Education, Tech Learning, Courses, Progress Tracking, Gamification',
  authors: [{ name: 'TechTots Team' }],
  icons: {
    icon: [
      {
        url: '/icon-light-32x32.png',
        media: '(prefers-color-scheme: light)',
      },
      {
        url: '/icon-dark-32x32.png',
        media: '(prefers-color-scheme: dark)',
      },
      {
        url: '/icon.svg',
        type: 'image/svg+xml',
      },
    ],
    apple: '/apple-icon.png',
  },
  openGraph: {
    title: 'TechTots LMS',
    description: 'Your platform for tech learning and growth',
    type: 'website',
    url: 'https://techtots.com',
  },
}

export const viewport: Viewport = {
  colorScheme: 'light dark',
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#ffffff' },
    { media: '(prefers-color-scheme: dark)', color: '#000000' },
  ],
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  userScalable: true,
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className="bg-background">
      <body className="antialiased text-foreground">
        <AuthProvider>{children}</AuthProvider>
        {process.env.NODE_ENV === 'production' && <Analytics />}
      </body>
    </html>
  )
}
