function renderInline(text) {
  const parts = text.split(/(\*\*.+?\*\*|`.+?`)/g)
  return parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={i}>{part.slice(2, -2)}</strong>
    }
    if (part.startsWith('`') && part.endsWith('`')) {
      return <code key={i}>{part.slice(1, -1)}</code>
    }
    return part
  })
}

export default function MessageBubble({ role, text, isError }) {
  const className = `msg ${role}${isError ? ' error' : ''}`
  return <div className={className}>{renderInline(text)}</div>
}