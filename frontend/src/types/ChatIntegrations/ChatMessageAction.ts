import { ChatMessageActionFields } from './ChatMessageActionFields'

export interface ChatMessageAction{
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
	/**	Action Name : Data	*/
	action_name: string
	/**	Enabled : Check	*/
	enabled?: 0 | 1
	/**	Action : Select	*/
	action: "Create Document" | "Custom Function"
	/**	Document Type : Link - DocType	*/
	document_type?: string
	/**	Custom Function Path : Small Text	*/
	custom_function_path?: string
	/**	Title : Data - Shown on the dialog	*/
	title: string
	/**	Description : Small Text	*/
	description?: string
	/**	Success Message : Small Text	*/
	success_message?: string
	/**	Fields : Table - Chat Message Action Fields	*/
	fields?: ChatMessageActionFields[]
}