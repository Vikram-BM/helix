import axios from 'axios';
import { Message, OutreachSequence, Session, User } from '../types';

const API_URL = process.env.REACT_APP_API_URL || '';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchSequences = async (): Promise<OutreachSequence[]> => {
  const response = await api.get('/sequences');
  return response.data;
};

export const fetchSequence = async (id: string): Promise<OutreachSequence> => {
  const response = await api.get(`/sequences/${id}`);
  return response.data;
};

export const createSequence = async (sequence: Partial<OutreachSequence>): Promise<OutreachSequence> => {
  const response = await api.post('/sequences', sequence);
  return response.data;
};

export const updateSequence = async (
  id: string, 
  updates: Partial<OutreachSequence>
): Promise<OutreachSequence> => {
  const response = await api.put(`/sequences/${id}`, updates);
  return response.data;
};

export const deleteSequence = async (id: string): Promise<void> => {
  await api.delete(`/sequences/${id}`);
};

export const updateOutreachStep = async (
  sequenceId: string,
  stepId: string,
  updates: Partial<OutreachSequence['steps'][0]>
): Promise<OutreachSequence> => {
  const response = await api.put(`/sequences/${sequenceId}/steps/${stepId}`, updates);
  return response.data;
};

export const fetchCurrentSession = async (): Promise<Session> => {
  const response = await api.get('/sessions/current');
  return response.data;
};

export const createSession = async (): Promise<Session> => {
  const response = await api.post('/sessions');
  return response.data;
};

export const sendMessage = async (message: Omit<Message, 'id' | 'timestamp'>): Promise<Message> => {
  const response = await api.post('/messages', message);
  return response.data;
};

export const getUserProfile = async (): Promise<User> => {
  const response = await api.get('/users/profile');
  return response.data;
};

export const updateUserProfile = async (updates: Partial<User>): Promise<User> => {
  const response = await api.put('/users/profile', updates);
  return response.data;
};

export default {
  fetchSequences,
  fetchSequence,
  createSequence,
  updateSequence,
  deleteSequence,
  updateOutreachStep,
  fetchCurrentSession,
  createSession,
  sendMessage,
  getUserProfile,
  updateUserProfile,
};