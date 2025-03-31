import React from 'react';
import { Message } from '../types';

interface ChatMessageProps {
  message: Message;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';
  const isLoading = message.loading;
  
  const renderToolCall = () => {
    if (!message.toolCall) return null;
    
    return (
      <div className="tool-call">
        <div className="tool-call-name">
          <span className="tool-call-badge">
            {message.toolCall.status === 'calling' ? 'Calling' : message.toolCall.status}
          </span>
          <span className="tool-call-text">{message.toolCall.name}</span>
        </div>
        {message.toolCall.result && (
          <div className="tool-call-result">
            <pre>{message.toolCall.result}</pre>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className={`chat-message ${isUser ? 'user-message' : 'assistant-message'}`}>
      <div className="message-avatar">
        {isUser ? 'You' : 'Helix'}
      </div>
      <div className="message-content">
        {isLoading ? (
          <div className="loading-indicator">
            <span className="dot"></span>
            <span className="dot"></span>
            <span className="dot"></span>
          </div>
        ) : (
          <>
            <div className="message-text">{message.content}</div>
            {renderToolCall()}
          </>
        )}
        <div className="message-timestamp">
          {new Date(message.timestamp).toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;