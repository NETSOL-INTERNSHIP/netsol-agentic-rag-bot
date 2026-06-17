import './MessageBubble.css'

interface Message {
  role: 'user' | 'bot'
  text: string
  sources?: string[]
}

export default function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === 'user'

  return (
    <div className={`bubble-wrapper ${isUser ? 'user' : 'bot'}`}>
      <div className={`bubble ${isUser ? 'user-bubble' : 'bot-bubble'}`}>
        <p>{message.text}</p>
        {!isUser && message.sources && (
          <div className="sources">
            {message.sources.map((s, i) => (
              <span key={i} className="source-tag">{s}</span>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}