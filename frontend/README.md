# Lumina Frontend

Modern Next.js 15 frontend for the Lumina AI visual search engine.

## Tech Stack
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **API Client**: Native Fetch API

## Project Structure
```
frontend/
├── app/              # Next.js app router
│   ├── layout.tsx   # Root layout
│   ├── page.tsx     # Landing page
│   └── search/      # Search page
├── components/       # React components
│   ├── ui/          # Reusable UI components
│   └── search/      # Search-specific components
├── lib/             # Utilities
│   ├── api-client.ts  # Backend API client
│   └── utils.ts       # Helper functions
└── types/           # TypeScript types
    └── api.ts       # API response types
```

## Development

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## Environment Variables

Create a `.env.local` file:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Features
- 🎨 Modern gradient UI design
- 📱 Fully responsive layout
- ⚡ Fast page loads with Next.js 15
- 🔍 Visual search interface (coming soon)
- 🖼️ Image upload with preview (coming soon)
