import StorageService from './storageService';
import ChatClient from '../clients/chatClient';

export interface ChatMessage {
    sender: 'user' | 'assistant',
    text: string
}


export interface Chat {
    id: string;
    createdAt: string;
    messages: ChatMessage[];
}



export default class ChatService {
    private storageService: StorageService
    private chatClient: ChatClient

    constructor() {
        this.storageService = new StorageService()
        this.chatClient = new ChatClient()
    }

    public async createChat(): Promise<string> {
        const chatId = await this.chatClient.createChat()
        this.storageService.createChat({ id: chatId })
        return chatId
    }

    public getChat({ id }: { id: string }): Chat {
        const chat = this.storageService.getChat({ id })
        return { id: chat.id, createdAt: chat.createdAt, messages: chat.messages.map(msg => ({ sender: msg.sender, text: msg.text })) }
    }

    public async sendMessage({ id, message }: { id: string, message: string }): Promise<ChatMessage> {
        const response: string = await this.chatClient.sendMessage(message)

        const newMessages: ChatMessage[] = [{ sender: 'user', text: response }, { sender: 'assistant', text: response }]
        this.storageService.updateChat({ id, newMessages })
        return { sender: 'assistant', text: response }
    }
}