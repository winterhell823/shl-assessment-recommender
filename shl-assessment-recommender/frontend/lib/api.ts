import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export async function sendMessageToAPI(messages: Message[]) {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://shl-assessment-recommender-9czk.onrender.com'
    const response = await fetch(`${apiUrl}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages,
      }),
    })

    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`)
    }

    return await response.json()
  } catch (error) {
    console.error('Failed to send message:', error)
    throw error
  }
}

export async function getRecommendations(query: string) {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://shl-assessment-recommender-9czk.onrender.com'
    const response = await fetch(`${apiUrl}/api/recommendations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    })

    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`)
    }

    return await response.json()
  } catch (error) {
    console.error('Failed to get recommendations:', error)
    throw error
  }
}
