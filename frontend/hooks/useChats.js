'use client';
import { useState, useEffect, useCallback } from 'react';
import { api } from '../lib/api';

export function useChats() {
  const [chats, setChats]   = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError]   = useState(null);

  const loadChats = useCallback(async () => {
    try {
      setLoading(true);
      const data = await api.getChats();
      setChats(data.chats || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { loadChats(); }, [loadChats]);

  const createChat = useCallback(async (tool, title) => {
    const data = await api.createChat(tool, title);
    setChats(prev => [data.chat, ...prev]);
    return data.chat;
  }, []);

  const deleteChat = useCallback(async (chatId) => {
    await api.deleteChat(chatId);
    setChats(prev => prev.filter(c => c.id !== chatId));
  }, []);

  const updateChatTitle = useCallback((chatId, title) => {
    setChats(prev => prev.map(c => c.id === chatId ? { ...c, title } : c));
  }, []);

  return { chats, loading, error, loadChats, createChat, deleteChat, updateChatTitle };
}
