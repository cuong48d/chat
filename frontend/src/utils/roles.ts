export const hasChatUserRole = () => {

    if (import.meta.env.DEV) {
        return true
    }
    //@ts-expect-error
    return (window?.frappe?.boot?.user?.roles ?? []).includes('Chat User');
}

export const hasChatAdminRole = () => {
    //@ts-expect-error
    return (window?.frappe?.boot?.user?.roles ?? []).includes('Chat Admin');
}

export const isSystemManager = () => {
    //@ts-expect-error
    return (window?.frappe?.boot?.user?.roles ?? []).includes('System Manager');
}

export const hasServerScriptEnabled = () => {
    if (import.meta.env.DEV) {
        return true
    }
    // @ts-expect-error
    return (window?.frappe?.boot?.server_script_enabled)
}