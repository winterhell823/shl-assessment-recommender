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
    console.log('[API] sendMessageToAPI called with URL:', apiUrl)
    console.log('[API] Sending messages:', messages)
    
    const response = await fetch(`${apiUrl}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages,
      }),
    })

    console.log('[API] Response status:', response.status, response.statusText)
    
    if (!response.ok) {
      const errorText = await response.text()
      console.error('[API] Error response body:', errorText)
      throw new Error(`API error: ${response.status} ${response.statusText} - ${errorText}`)
    }

    const data = await response.json()
    console.log('[API] Response data:', data)
    return data
  } catch (error) {
    console.error('[API] Error in sendMessageToAPI:', error)
    throw error
  }
}

export async function getRecommendations(query: string) {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://shl-assessment-recommender-9czk.onrender.com'
    console.log('[API] getRecommendations called with URL:', apiUrl)
    console.log('[API] Query:', query)
    
    const response = await fetch(`${apiUrl}/api/recommendations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    })

    console.log('[API] Response status:', response.status, response.statusText)
    
    if (!response.ok) {
      const errorText = await response.text()
      console.error('[API] Error response body:', errorText)
      throw new Error(`API error: ${response.status} ${response.statusText} - ${errorText}`)
    }

    const data = await response.json()
    console.log('[API] Response data:', data)
    return data
  } catch (error) {
    console.error('[API] Error in getRecommendations:', error)
    throw error
  }
}
