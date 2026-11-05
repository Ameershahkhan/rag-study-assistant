import { useEffect, useState } from 'react'
import { getWeakTopics } from '../api'

export default function TopicsPanel({ refreshKey }) {
  const [topics, setTopics] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    getWeakTopics()
      .then((t) => {
        setTopics(t)
        setError('')
      })
      .catch((err) => setError(err.message))
  }, [refreshKey])

  return (
    <aside className="side">
      <h2>Topics to review</h2>
      {error && <p className="muted">{error}</p>}
      {topics && topics.length === 0 && (
        <p className="muted">No quiz results yet. Ask me to quiz you.</p>
      )}
      {topics &&
        topics.map((t) => (
          <div className="topic" key={t.topic}>
            <span>{t.topic}</span>
            <span>
              {t.correct}/{t.total}
            </span>
          </div>
        ))}
    </aside>
  )
}