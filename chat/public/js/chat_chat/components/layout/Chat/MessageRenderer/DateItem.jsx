import React from 'react'

const DateItem = ({ date }) => {
    return (
        <div className='chat-date-separator'>
            <div className='chat-date-separator-line'>

            </div>
            <div className='chat-date-separator-text'>
                {moment(date, frappe.defaultDatetimeFormat).format('Do MMMM YYYY')}
            </div>
            <div className='chat-date-separator-line'></div>
        </div>
    )
}

export default DateItem