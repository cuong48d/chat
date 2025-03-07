
export interface ChatPollVote{
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
	/**	User : Link - Chat User	*/
	user_id: string
	/**	Poll : Link - Chat Poll	*/
	poll_id: string
	/**	Option : Data	*/
	option: string
}