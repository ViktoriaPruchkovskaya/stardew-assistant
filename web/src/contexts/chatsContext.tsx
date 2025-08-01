import { createContext, ReactNode } from "react";
import { ChatMetadata } from "../services/ChatService";

export interface ChatsContextProps {
    chatIds: string[];
    createChat: () => Promise<ChatMetadata>;
    deleteChats: (ids: string[]) => Promise<void>;
}

interface ChatsContextPropsWithChildren extends ChatsContextProps {
    children: ReactNode
}

export const ChatsContext = createContext<ChatsContextProps | null>(null);

export default function ChatsProvider({ children, chatIds, createChat, deleteChats }: ChatsContextPropsWithChildren) {
    return (<ChatsContext.Provider value={{ chatIds, createChat, deleteChats }}>
        {children}
    </ChatsContext.Provider >)
}