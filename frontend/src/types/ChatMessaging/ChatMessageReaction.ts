
export interface ChatMessageReaction{
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
	/**	Reaction : Data	*/
	reaction: string
	/**	Reaction Escaped : Data	*/
	reaction_escaped?: string
	/**	Message : Link - Chat Message	*/
	message: string
	/**	Channel ID : Link - Chat Channel	*/
	channel_id?: string
	/**	Is Custom : Check	*/
	is_custom?: 0 | 1
}