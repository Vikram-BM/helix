export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  loading?: boolean;
  toolCall?: ToolCall;
}

export interface ToolCall {
  name: string;
  status: 'calling' | 'completed' | 'failed';
  result?: string;
}

export interface OutreachStep {
  id: string;
  stepNumber: number;
  type: 'email' | 'linkedin' | 'phone' | 'other';
  content: string;
  subject?: string;
  timing?: string;
  waitTime?: number;
}

export interface OutreachSequence {
  id: string;
  name: string;
  companyName: string;
  roleName: string;
  candidatePersona: string;
  steps: OutreachStep[];
  createdAt: Date;
  updatedAt: Date;
}

export interface User {
  id: string;
  name: string;
  email: string;
  company?: string;
  role?: string;
  preferences?: Record<string, any>;
}

export interface Session {
  id: string;
  userId: string;
  currentSequenceId?: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
}