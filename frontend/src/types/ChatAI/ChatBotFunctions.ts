
export interface ChatBotFunctions{
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
	/**	Function : Link - Chat AI Function	*/
	function: string
	/**	Type : Data	*/
	type?: string
	/**	Description : Small Text	*/
	description?: string
}