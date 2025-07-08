
interface ChatMessage {
    sender: 'user' | 'assistant',
    text: string
}

interface Chat {
    id: string;
    createdAt: string;
    messages: ChatMessage[];
}

export default class ChatClient {
    private readonly baseUrl = "http://localhost:8000/api/chat"
    public async sendMessage({ id, message }: { id: string, message: string }): Promise<string> {
        const res = await fetch(`${this.baseUrl}/${id}`, {
            method: "POST", headers: {
                'Content-Type': 'application/json'
            }, body: JSON.stringify({ message })
        })
        const parsed = await res.json()
        return parsed.message
    }

    public async createChat(): Promise<string> {
        const res = await fetch(`${this.baseUrl}`, {
            method: "POST", headers: {
                'Content-Type': 'application/json'
            }
        })
        const parsed = await res.json()
        return parsed.id
    }

    public async getChat({ id }: { id: string }): Promise<Chat> {
        const res = await fetch(`${this.baseUrl}/${id}`, {
            method: "GET", headers: {
                'Content-Type': 'application/json'
            }
        })
        const parsed = await res.json()
        return { id: parsed._id, createdAt: parsed.created_at, messages: parsed.message.map(msg => ({ sender: msg.role, text: msg.text })) }
    }
}