$(document).on('app_ready', function () {
    if (frappe.boot.show_chat_chat_on_desk && frappe.user.has_role("Chat User")) {

        // If on mobile, do not show the chat
        if (frappe.is_mobile()) {
            return;
        }
        let main_section = $(document).find('.main-section');

        // Add bottom padding to the main section
        main_section.css('padding-bottom', '60px');

        let chat_element = $(document.createElement('div'));
        chat_element.addClass('chat-chat');

        main_section.append(chat_element);

        frappe.require("chat_chat.bundle.jsx").then(() => {
            frappe.chat_chat = new frappe.ui.ChatChat({
                wrapper: chat_element,
            });
        });
    }

});
import './templates/send_message.html';
import './timeline_button';
