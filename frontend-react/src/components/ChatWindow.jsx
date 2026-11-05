import { useEffect, useRef, useState } from 'react'
import MessageBubble from './MessageBubble'
import { sendMessage } from '../api'

const GREETING = {
  role: 'bot',
  text: 'Hi! Ask me about your lectures, or say: Quiz me on embeddings.',
}

export default function ChatWindow({ onReply }) {
  const [messages, setMessages] = useState([GREETING])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [sessionId, setSessionId] = useState(null)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  async function handleSubmit(e) {
    e.preventDefault()
    const text = input.trim()
    if (!text || loading) return

    setInput('')
    setMessages((prev) => [...prev, { role: 'user', text }])
    setLoading(true)

    try {
      const data = await sendMessage(text, sessionId)
      setSessionId(data.session_id)
      setMessages((prev) => [...prev, { role: 'bot', text: data.reply }])
      onReply()
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: 'bot', text: err.message, isError: true },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="chat">
      <h1>RAG Study Assistant</h1>
      <div className="messages">
        {messages.map((m, i) => (
          <MessageBubble key={i} {...m} />
        ))}
        {loading && <MessageBubble role="bot" text="Thinking..." />}
        <div ref={bottomRef} />
      </div>
      <form onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about your lectures..."
          autoComplete="off"
        />
        <button type="submit" disabled={loading}>
          Send
        </button>
      </form>
    </section>
  )
}