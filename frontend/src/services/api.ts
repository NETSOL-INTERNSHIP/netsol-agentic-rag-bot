import axios from 'axios'

const API_BASE = 'http://localhost:8090'

interface ChatResponse {
  answer: string
  sources: string[]
}

export async function sendMessage(question: string): Promise<ChatResponse> {
  const res = await axios.post(`${API_BASE}/chat`, { question })
  return res.data
}

export async function triggerIngest(): Promise<{ status: string }> {
  const res = await axios.post(`${API_BASE}/ingest`)
  return res.data
}