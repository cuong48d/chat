
export interface ChatHRCompanyWorkspace{
	creation: string
	name: string
	modified: string
	owner: string
	modified_by: string
	docstatus: 0 | 1 | 2
	parent?: string
	parentfield?: string
	parenttype?: string
	idx?: number
	/**	Company : Data - Link to the company	*/
	company: string
	/**	Chat Workspace : Link - Chat Workspace	*/
	chat_workspace: string
}