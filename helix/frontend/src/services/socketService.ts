import { io, Socket } from 'socket.io-client';
import { Message, OutreachSequence } from '../types';

class SocketService {
  private socket: Socket | null = null;
  private messageListeners: ((message: Message) => void)[] = [];
  private sequenceUpdateListeners: ((sequence: OutreachSequence) => void)[] = [];
  private toolCallListeners: ((toolCall: Message) => void)[] = [];

  connect() {
    if (!this.socket) {
      this.socket = io(process.env.REACT_APP_SOCKET_URL || '');
      
      this.setupListeners();
    }
    return this.socket;
  }

  private setupListeners() {
    if (!this.socket) return;
    
    this.socket.on('message', (message: Message) => {
      this.messageListeners.forEach(listener => listener(message));
    });
    
    this.socket.on('sequence_update', (sequence: OutreachSequence) => {
      this.sequenceUpdateListeners.forEach(listener => listener(sequence));
    });
    
    this.socket.on('tool_call', (toolCall: Message) => {
      this.toolCallListeners.forEach(listener => listener(toolCall));
    });
  }

  sendMessage(message: Omit<Message, 'id' | 'timestamp'>) {
    if (!this.socket) this.connect();
    this.socket?.emit('message', message);
  }

  updateSequence(sequence: Partial<OutreachSequence> & { id: string }) {
    if (!this.socket) this.connect();
    this.socket?.emit('update_sequence', sequence);
  }

  onMessage(callback: (message: Message) => void) {
    this.messageListeners.push(callback);
    return () => {
      this.messageListeners = this.messageListeners.filter(listener => listener !== callback);
    };
  }

  onSequenceUpdate(callback: (sequence: OutreachSequence) => void) {
    this.sequenceUpdateListeners.push(callback);
    return () => {
      this.sequenceUpdateListeners = this.sequenceUpdateListeners.filter(listener => listener !== callback);
    };
  }

  onToolCall(callback: (toolCall: Message) => void) {
    this.toolCallListeners.push(callback);
    return () => {
      this.toolCallListeners = this.toolCallListeners.filter(listener => listener !== callback);
    };
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
      this.messageListeners = [];
      this.sequenceUpdateListeners = [];
      this.toolCallListeners = [];
    }
  }
}

export const socketService = new SocketService();
export default socketService;