import { useFrappeGetCall } from 'frappe-react-sdk'
import { ChatWorkspace } from '@/types/Chat/ChatWorkspace'

export type WorkspaceFields = Pick<ChatWorkspace, 'name' | 'workspace_name' | 'logo' | 'type' | 'can_only_join_via_invite' | 'description'> & {
    workspace_member_name?: string
    is_admin?: 0 | 1
}

const useFetchWorkspaces = () => {
    return useFrappeGetCall<{ message: WorkspaceFields[] }>('chat.api.workspaces.get_list', undefined, 'workspaces_list', {
        revalidateOnFocus: false,
        keepPreviousData: true
    })
}

export default useFetchWorkspaces