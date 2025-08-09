
type Sender = 'user' | 'assistant'

interface ChatMessage {
    sender: Sender,
    text: string
}
interface CreatedChat {
    id: string;
    createdAt: string;
}
interface Chat {
    id: string;
    createdAt: string;
    messages: ChatMessage[];
}

export default class ChatClient {
    private readonly baseUrl = "/api/chat"
    private readonly headers = {
        'Content-Type': 'application/json'
    }
    public async sendMessage({ id, message }: { id: string, message: string }): Promise<string> {
        const res = await fetch(`${this.baseUrl}/${id}`, {
            method: "POST", headers: this.headers, body: JSON.stringify({ message })
        })
        const parsed = await res.json()
        return parsed.message
    }

    public async createChat(): Promise<CreatedChat> {
        const res = await fetch(`${this.baseUrl}`, {
            method: "POST", headers: this.headers
        })
        const parsed = await res.json()
        return { id: parsed._id, createdAt: parsed.created_at }
    }

    public async deleteChats({ ids }: { ids: string[] }): Promise<void> {
        await fetch(`${this.baseUrl}`, { method: "DELETE", headers: this.headers, body: JSON.stringify({ ids }) })
    }

    public async getChat({ id }: { id: string }): Promise<Chat> {
        const res = await fetch(`${this.baseUrl}/${id}`, {
            method: "GET", headers: this.headers
        })
        const parsed = await res.json()
        return {
            id: parsed._id,
            createdAt: parsed.created_at,
            messages: parsed.messages.map((msg: { role: Sender, content: string }) => ({ sender: msg.role, text: msg.content }))
        }
    }
}