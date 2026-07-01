# SHL Assessment Recommender - Frontend

A modern, responsive React frontend for the SHL Assessment Recommender with a green-white theme.

## Tech Stack

- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **Lucide React** - Icons
- **shadcn/ui** - Component library

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create `.env.local` file with your configuration:
```bash
cp .env.local.example .env.local
```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure

```
frontend/
├── app/                 # Next.js app directory
│   ├── page.tsx        # Home page
│   └── layout.tsx      # Root layout
├── components/
│   └── ui/             # Reusable components
│       └── animated-ai-chat.tsx
├── lib/
│   └── utils.ts        # Utility functions
├── styles/
│   └── globals.css     # Global styles
├── public/             # Static assets
├── tailwind.config.ts  # Tailwind configuration
└── tsconfig.json       # TypeScript configuration
```

## Features

- ✨ Animated AI chat interface
- 🎨 Green-white color theme
- 📱 Fully responsive design
- ⌨️ Keyboard shortcuts and command palette
- 🎭 Smooth animations with Framer Motion
- 📎 File attachment support
- 🎯 Smart command suggestions

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Environment Variables

Key environment variables:
- `NEXT_PUBLIC_API_URL` - Backend API endpoint

## Theme Customization

The green-white theme is defined in `styles/globals.css` and uses CSS custom properties. Modify the color values to customize the theme:

- `--color-primary` - Main green color (currently 142 76% 36%)
- `--color-secondary` - Secondary green (currently 120 100% 50%)
- Light/dark mode variants are also available

## Contributing

1. Create a new branch
2. Make your changes
3. Commit with clear messages
4. Push and create a pull request

## License

This project is part of the SHL Assessment Recommender system.
