
export interface ChatBotAIPrompt{
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
	/**	Prompt : Small Text	*/
	prompt: string
	/**	Naming Series : Select	*/
	naming_series?: "PR-.#####."
	/**	Chat Bot : Link - Chat Bot - If added, this prompt will only be shown when interacting with the bot	*/
	chat_bot?: string
	/**	Is Global : Check - If checked, this prompt will be available to all users on Chat	*/
	is_global?: 0 | 1
}