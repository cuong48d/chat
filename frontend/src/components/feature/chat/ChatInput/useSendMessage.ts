import { useFrappePostCall } from 'frappe-react-sdk'
import { Message } from '../../../../../../types/Messaging/Message'
import { ChatMessage } from '@/types/ChatMessaging/ChatMessage'

export const useSendMessage = (channelID: string, uploadFiles: (selectedMessage?: Message | null) => Promise<ChatMessage[]>, onMessageSent: (messages: ChatMessage[]) => void, selectedMessage?: Message | null) => {

    const { call, loading } = useFrappePostCall<{ message: ChatMessage }>('chat.api.chat_message.send_message')

    const sendMessage = async (content: string, json?: any): Promise<void> => {

        if (content) {
            return call({
                channel_id: channelID,
                text: content,
                json_content: json,
                is_reply: selectedMessage ? 1 : 0,
                linked_message: selectedMessage ? selectedMessage.name : null
            })
                .then((res) => onMessageSent([res.message]))
                .then(() => uploadFiles())
                .then((res) => {
                    onMessageSent(res)
                })
        } else {
            return uploadFiles(selectedMessage)
                .then((res) => {
                    onMessageSent(res)
                })
        }
    }


    return {
        sendMessage,
        loading
    }
}