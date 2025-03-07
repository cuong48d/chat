import { useFrappeGetCall } from "frappe-react-sdk"
import useChatSettings from "./useChatSettings"

const useIsUserOnLeave = (user: string) => {

    // Check if leave status needs to be shown
    const { chatSettings } = useChatSettings()

    //@ts-expect-error
    const isHRInstalled = window?.frappe?.boot?.versions?.hrms !== undefined

    const { data } = useFrappeGetCall<{ message: boolean }>("chat.api.chat_users.is_user_on_leave", {
        user: user
    }, chatSettings?.show_if_a_user_is_on_leave && isHRInstalled ? ["is_user_on_leave", user] : null, {
        // Refresh every 6 hours or on page refresh
        dedupingInterval: 6 * 60 * 60 * 1000,
        revalidateOnFocus: false
    })

    return data?.message ?? false

}

export default useIsUserOnLeave