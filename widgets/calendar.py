from types import coroutine
from aiogram.types import *
from controller import bot
from widgets import Button
import calendar
import datetime


class Calendar:
    def __init__(
        self,
        message: Message,
        click_action: coroutine,
        start_month: int = None,
        show_current_month: bool = True,
        show_current_day: bool = True,
        prev_page_sign: str = "<--",
        next_page_sign: str = "-->",
    ):
        self.message = message
        self.show_current_month = show_current_month
        self.show_current_day = show_current_day
        self.click_action = click_action

        self.next_page = Button(text=next_page_sign)
        self.previous_page = Button(text=prev_page_sign)

        today = datetime.datetime.today()

        if start_month is None or start_month not in range(1, 13):
            self.current_month = today.month

        self.current_year = today.year

    async def handle_chosen_date(self, callback: CallbackQuery, chosen_date: int):
        date = datetime.datetime(self.current_year, self.current_month, chosen_date)

        await self.click_action(date)

    async def render_page(self):
        inline_keyboard = list()
        if self.show_current_month:
            current_data_btn = Button(
                text=calendar.month_name[self.current_month] + f" [{self.current_year}]"
            )
            inline_keyboard.append([current_data_btn])

        weeks = calendar.Calendar().monthdayscalendar(
            self.current_year, self.current_month
        )

        for week in weeks:
            replaced = list()
            for day in week:
                header = str(day) if day else " "

                today = datetime.datetime.today()
                if (
                    str(today.day) == header
                    and self.current_month == today.month
                    and self.current_year == today.year
                    and self.show_current_day
                ):

                    header = "[ " + header + " ]"

                day_button = Button(text=header)
                if day:
                    day_button.onClick(self.handle_chosen_date, day)

                replaced.append(day_button)

            # self.markup.row(*replaced)
            inline_keyboard.append([*replaced])

        self.previous_page.onClick(self.go_to_previous_page)
        self.next_page.onClick(self.go_to_next_page)

        # self.markup.row(self.previous_page, self.next_page)
        inline_keyboard.append([self.previous_page, self.next_page])
        self.markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

        await bot.edit_message_reply_markup(
            self.message.chat.id, self.message.message_id, reply_markup=self.markup
        )

    async def go_to_next_page(self, callback: CallbackQuery):
        if self.current_month + 1 <= 12:
            self.current_month += 1

            await self.render_page()
            return

        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1

            await self.render_page()

    async def go_to_previous_page(self, callback: CallbackQuery):
        if self.current_month - 1 > 0:
            self.current_month -= 1

            await self.render_page()
            return

        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
            
            await self.render_page()

