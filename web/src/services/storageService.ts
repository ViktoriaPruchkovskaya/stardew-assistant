import { Chat, ChatMessage } from "./ChatService"


export default class StorageService {
    public createChat({ id, createdAt }: {
        id: string,
        createdAt: string
    }) {
        localStorage.setItem(id, JSON.stringify({ createdAt, messages: [] }))
    }

    public getChat({ id }: {
        id: string
    }): Chat {
        console.log(id)
        const record = localStorage.getItem(id)
        console.log(record)
        if (!record) {
            throw new Error('Could not retrieve chat')
        }
        const chat = JSON.parse(record)
        return {
            id: chat.id,
            createdAt: chat.createdAt,
            messages: chat.messages
        }
    }

    public updateChat({ id, newMessages }: { id: string, newMessages: ChatMessage[] }) {
        console.log(id)
        const chat: Chat = this.getChat({ id })
        const { id: chatId, ...data } = { ...chat, messages: [...chat.messages, ...newMessages] }

        localStorage.setItem(id, JSON.stringify(data))
    }
}