import { ChatSettings } from "@/types/Chat/ChatSettings"
import { useFrappeGetDoc } from "frappe-react-sdk"

const useChatSettings = () => {

    const { data, mutate } = useFrappeGetDoc<ChatSettings>("Chat Settings", "Chat Settings", "chat_settings", {
        revalidateOnFocus: false,
        // Refresh every 8 hours or on page refresh
        dedupingInterval: 8 * 60 * 60 * 1000
    })

    return {
        chatSettings: data,
        mutate
    }
}

export default useChatSettings