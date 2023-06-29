from aiogram.types import *
from controller import bot
from widgets import Button
import calendar
import datetime


class Calendar():
    def __init__(
        self,
        message: Message,
        start_month: int = None,
        show_current_month: bool = True,
        show_current_day: bool = True,
        prev_page_sign: str = '<--',
        next_page_sign: str = '-->'
    ):
        self.message = message
        self.show_current_month = show_current_month
        self.show_current_day = show_current_day

        self.next_page = Button(next_page_sign)
        self.previous_page = Button(prev_page_sign)

        today = datetime.datetime.today()

        if start_month is None or start_month not in range(1, 13):
            self.current_month = today.month

        self.current_year = today.year

    async def render_page(self):
        self.markup = InlineKeyboardMarkup()

        if self.show_current_month:
            self.markup.add(Button(calendar.month_name[self.current_month]))

        weeks = calendar.Calendar().monthdayscalendar(
            self.current_year, self.current_month)

        for week in weeks:
            replaced = list()
            for day in week:
                header = str(day) if day else ' '

                today = datetime.datetime.today()
                if str(today.day) == header \
                        and self.current_month == today.month \
                        and self.show_current_day:

                    header = '[ ' + header + ' ]'

                replaced.append(Button(header))

            self.markup.row(*replaced)

        self.previous_page.onClick(self.go_to_previous_page)
        self.next_page.onClick(self.go_to_next_page)

        self.markup.row(self.previous_page, self.next_page)

        await bot.edit_message_reply_markup(
            self.message.chat.id,
            self.message.message_id,
            reply_markup=self.markup
        )

    async def go_to_next_page(self, callback: CallbackQuery):
        if self.current_month + 1 <= 12:
            self.current_month += 1

            await self.render_page()

    async def go_to_previous_page(self, callback: CallbackQuery):
        if self.current_month - 1 > 0:
            self.current_month -= 1

            await self.render_page()
