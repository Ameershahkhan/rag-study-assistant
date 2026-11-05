import { useState } from 'react'
import ChatWindow from './components/ChatWindow'
import TopicsPanel from './components/TopicsPanel'
import './App.css'

export default function App() {
  const [refreshKey, setRefreshKey] = useState(0)

  return (
    <div className="app">
      <ChatWindow onReply={() => setRefreshKey((k) => k + 1)} />
      <TopicsPanel refreshKey={refreshKey} />
    </div>
  )
}