import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { Message, OutreachSequence, Session, User } from '../types';
import * as apiService from '../services/apiService';
import socketService from '../services/socketService';
import { v4 as uuidv4 } from 'uuid';

interface AppContextType {
  messages: Message[];
  sequence: OutreachSequence | null;
  user: User | null;
  session: Session | null;
  isLoading: boolean;
  sendMessage: (content: string) => void;
  updateSequence: (updates: Partial<OutreachSequence>) => void;
  updateStep: (stepId: string, updates: Partial<OutreachSequence['steps'][0]>) => void;
  updateUser: (updates: Partial<User>) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [sequence, setSequence] = useState<OutreachSequence | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const initializeApp = async () => {
      try {
        socketService.connect();
        
        const sessionResponse = await apiService.fetchCurrentSession()
          .catch(() => apiService.createSession());
        
        setSession(sessionResponse);
        setMessages(sessionResponse.messages);
        
        if (sessionResponse.currentSequenceId) {
          const sequenceResponse = await apiService.fetchSequence(sessionResponse.currentSequenceId);
          setSequence(sequenceResponse);
        }
        
        const userResponse = await apiService.getUserProfile().catch(() => null);
        if (userResponse) {
          setUser(userResponse);
        }
      } catch (error) {
        console.error('Failed to initialize app:', error);
      } finally {
        setIsLoading(false);
      }
    };

    initializeApp();

    return () => {
      socketService.disconnect();
    };
  }, []);

  useEffect(() => {
    const messageUnsubscribe = socketService.onMessage((message) => {
      setMessages(prev => [...prev, message]);
    });

    const sequenceUnsubscribe = socketService.onSequenceUpdate((updatedSequence) => {
      setSequence(updatedSequence);
    });

    const toolCallUnsubscribe = socketService.onToolCall((toolCallMessage) => {
      setMessages(prev => {
        const messageIndex = prev.findIndex(m => m.id === toolCallMessage.id);
        if (messageIndex >= 0) {
          const newMessages = [...prev];
          newMessages[messageIndex] = toolCallMessage;
          return newMessages;
        }
        return [...prev, toolCallMessage];
      });
    });

    return () => {
      messageUnsubscribe();
      sequenceUnsubscribe();
      toolCallUnsubscribe();
    };
  }, []);

  const sendMessage = async (content: string) => {
    const tempId = uuidv4();
    const tempMessage: Message = {
      id: tempId,
      role: 'user',
      content,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, tempMessage]);

    try {
      const message = await apiService.sendMessage({
        role: 'user',
        content,
      });

      setMessages(prev => 
        prev.map(m => m.id === tempId ? message : m)
      );

      socketService.sendMessage({
        role: 'user',
        content,
      });
    } catch (error) {
      console.error('Failed to send message:', error);
      setMessages(prev => 
        prev.filter(m => m.id !== tempId)
      );
    }
  };

  const updateSequence = async (updates: Partial<OutreachSequence>) => {
    if (!sequence) return;

    try {
      const updatedSequence = await apiService.updateSequence(sequence.id, updates);
      setSequence(updatedSequence);
      socketService.updateSequence({
        id: sequence.id,
        ...updates,
      });
    } catch (error) {
      console.error('Failed to update sequence:', error);
    }
  };

  const updateStep = async (stepId: string, updates: Partial<OutreachSequence['steps'][0]>) => {
    if (!sequence) return;

    try {
      const updatedSequence = await apiService.updateOutreachStep(sequence.id, stepId, updates);
      setSequence(updatedSequence);
    } catch (error) {
      console.error('Failed to update step:', error);
    }
  };

  const updateUser = async (updates: Partial<User>) => {
    if (!user) return;

    try {
      const updatedUser = await apiService.updateUserProfile(updates);
      setUser(updatedUser);
    } catch (error) {
      console.error('Failed to update user:', error);
    }
  };

  return (
    <AppContext.Provider
      value={{
        messages,
        sequence,
        user,
        session,
        isLoading,
        sendMessage,
        updateSequence,
        updateStep,
        updateUser,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useApp = (): AppContextType => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};