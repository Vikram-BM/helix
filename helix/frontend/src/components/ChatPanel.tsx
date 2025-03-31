import React, { useEffect, useRef } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import { Message } from '../types';

interface ChatPanelProps {
  messages: Message[];
  onSendMessage: (content: string) => void;
  isLoading?: boolean;
}

const ChatPanel: React.FC<ChatPanelProps> = ({ 
  messages, 
  onSendMessage, 
  isLoading 
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="chat-panel">
      <div className="chat-header">
        <h2>Chat with Helix</h2>
      </div>
      
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="empty-messages">
            <p>Start a conversation with Helix to create outreach sequences!</p>
          </div>
        ) : (
          messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <ChatInput 
        onSendMessage={onSendMessage} 
        disabled={isLoading}
      />
    </div>
  );
};

export default ChatPanel;