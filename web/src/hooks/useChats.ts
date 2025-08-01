import { useEffect, useState } from "react"
import ChatService, { ChatMetadata } from "../services/ChatService"
import StorageService from "../services/storageService"

interface ChatsData {
    chatIds: string[];
    createChat: () => Promise<ChatMetadata>;
    deleteChats: (ids: string[]) => Promise<void>
}

export default function useChatsData(): ChatsData {
    const storageService = new StorageService()
    const chatService = new ChatService()
    const [chatIds, setChatIds] = useState<string[]>([])

    useEffect(() => {
        setChatIds(storageService.getChatIds())
    }, [])

    const createChat = async (): Promise<ChatMetadata> => {
        const chat = await chatService.createChat()
        setChatIds(prev => [...prev, chat.id])
        return chat
    }

    const deleteChats = async (ids: string[]) => {
        await chatService.deleteChats({ ids })
        storageService.deleteChats()
        setChatIds([])
    }

    return { chatIds, createChat, deleteChats }
}