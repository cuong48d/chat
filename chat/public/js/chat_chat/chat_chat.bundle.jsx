import * as React from "react";
import { App } from "./App";
import { createRoot } from "react-dom/client";


class ChatChat {
	constructor({ wrapper }) {
		this.$wrapper = $(wrapper);

		this.init();
	}

	init() {
		this.setup_app();
	}

	setup_app() {
		// create and mount the react app
		const root = createRoot(this.$wrapper.get(0));
		root.render(<App />);
		this.$chat_chat = root;
	}
}

frappe.provide("frappe.ui");
frappe.ui.ChatChat = ChatChat;
export default ChatChat;