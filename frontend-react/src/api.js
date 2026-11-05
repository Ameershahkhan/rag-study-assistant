export async function sendMessage(message, sessionId) {
  const res = await fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, session_id: sessionId }),
  })
  const data = await res.json()
  if (!res.ok) throw new Error(data.error || 'Request failed')
  return data
}

export async function getWeakTopics() {
  const res = await fetch('/weak-topics')
  if (!res.ok) throw new Error('Could not load topics')
  const data = await res.json()
  return data.topics
}