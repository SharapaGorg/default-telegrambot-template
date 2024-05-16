"""
Absolutely not useful with aiogram 3.x

Reasons:
1) aiogram does not provide any way to destroy message handler
2) somehow message handler is hashing and do not disappear => all futher calls of this handler does not have any effect
3) state does not clear for some reason, looks like it is not implementable in dynamic way

As a result first call of message handler is the onliest one and futher ones just call the first one

May be it is even better to implement question chain through database interaction,
it would be stable and, moreover, artificial database states does not clear after
bot reload or timeout

"""


from types import coroutine
from aiogram.types import *
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from async_class import AsyncClass
from controller import bot, dp
from widgets import Button
import random, string

class QuestionsChain(AsyncClass):
    class AnswerModel(StatesGroup):
        example_of_state_field = State()

    async def __ainit__(
        self,
        target_id: int,
        chain: dict,
        after_complete: coroutine,
        context: FSMContext,
        break_with_command: bool = False,
        first_button: Button = None,  # make back button for the first question
    ):
        """
        target_id : int - telegram ID of the person who will answer the chain of questions
        chain : dict - questions chain, format: { question_key : question }, example: { 'name' : 'What is your name?' }
        after_complete : async coroutine with dict arg, example: async some_function(answers : dict)

        !WARNING! this object works only with text messages (aiogram restrictions)
        """

        self.target_id = target_id
        self.chain = chain

        self.state = context
        self.first_button = first_button

        self.questions = list(chain.values())
        self.quest_keys = list(chain.keys())

        self.current_quest_key = int()
        self.answers = dict()

        self.complete_coroutine = after_complete

        # generating encoding key to avoid conflicts with the same @dp.message(field) - field is the same
        self.encoding_key = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(32)
        )

        for question_key in self.quest_keys:
            setattr(
                self.AnswerModel,
                question_key + self.encoding_key,
                State(),
            )

    async def activate(self):
        await self.__ask(self.questions[0], self.quest_keys[0], self.state, True)

    async def __ask(
        self, question: str, field_name: str, state: FSMContext, is_first_question=False
    ):
        
        print("ASK:", self.encoding_key)
        field = getattr(self.AnswerModel, field_name + self.encoding_key)
        await state.set_state(field)

        if is_first_question and self.first_button is not None:
            await bot.send_message(
                self.target_id,
                question,
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[self.first_button]]
                ),
            )
        else:
            await bot.send_message(self.target_id, question)

        self.current_quest_key += 1

        @dp.message(field)
        async def get_answer_of_my_dear_question(message: Message, state: FSMContext):
            print("INTERNAL HANDLER:", self.encoding_key)
            self.answers[self.quest_keys[self.current_quest_key - 1]] = message.text

            await state.update_data(
                data={self.quest_keys[self.current_quest_key - 1]: message.text}
            )
    
            if self.current_quest_key == len(self.quest_keys):
                await state.clear()
                await self.complete_coroutine(self.answers)

                return

            await self.__ask(
                self.questions[self.current_quest_key],
                self.quest_keys[self.current_quest_key],
                state,
            )

        
