from aiogram.types import *
from controller import dp, bot
from widgets import Button


class ButtonSlider:
    def __init__(
        self,
        message: Message,
        buttons: list[Button],
        rows: int = 5,
        columns: int = 1,
        prev_page_sign: str = '<--',
        next_page_sign: str = '-->'
    ):
        self.next_page = Button(next_page_sign)
        self.previous_page = Button(prev_page_sign)

        self.message = message
        self.buttons = buttons
        self.rows = rows
        self.columns = columns

        self.current_page = 0

    async def render_page(self):
        self.markup = InlineKeyboardMarkup()

        start_point = self.current_page * self.rows * self.columns
        for i in range(start_point, start_point + self.rows * self.columns, self.columns):
            buttons_in_row = list()

            for k in range(self.columns):
                try:
                    buttons_in_row.append(self.buttons[i + k])
                except IndexError:
                    break

            self.markup.row(*buttons_in_row)

        self.previous_page.onClick(self.go_to_previous_page)
        self.next_page.onClick(self.go_to_next_page)

        self.markup.row(self.previous_page, self.next_page)

        await bot.edit_message_reply_markup(
            self.message.chat.id,
            self.message.message_id,
            reply_markup=self.markup
        )

    async def go_to_next_page(self, callback: CallbackQuery):
        if len(self.buttons) > (self.current_page + 1) * self.rows * self.columns:
            self.current_page += 1

            await self.render_page()

    async def go_to_previous_page(self, callback: CallbackQuery):
        if self.current_page - 1 >= 0:
            self.current_page -= 1

            await self.render_page()
