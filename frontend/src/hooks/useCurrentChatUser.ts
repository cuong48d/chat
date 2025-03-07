import { ChatUser } from '@/types/Chat/ChatUser'
import { useFrappeGetCall } from 'frappe-react-sdk'

const useCurrentChatUser = () => {

    const { data, mutate } = useFrappeGetCall<{ message: ChatUser }>('chat.api.chat_users.get_current_chat_user',
        undefined,
        'my_profile',
        {
            // revalidateIfStale: false,
            revalidateOnFocus: false,
            shouldRetryOnError: false,
            revalidateOnReconnect: true
        }
    )

    return {
        myProfile: data?.message,
        mutate
    }

}

export default useCurrentChatUser