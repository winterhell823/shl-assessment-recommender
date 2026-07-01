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
    console.log('[API] sendMessageToAPI called with same-origin /api/chat route')
    console.log('[API] Sending messages:', messages)

    const response = await fetch('/api/chat', {
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
    console.log('[API] getRecommendations called with same-origin /api/recommendations route')
    console.log('[API] Query:', query)

    const response = await fetch('/api/recommendations', {
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
