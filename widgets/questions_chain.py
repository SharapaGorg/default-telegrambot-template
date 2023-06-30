from types import coroutine
from aiogram.types import *
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from async_class import AsyncClass
from controller import bot, dp


class QuestionsChain(AsyncClass):
    class AnswerModel(StatesGroup):
        example_of_state_field = State()

    async def __ainit__(
        self, 
        target_id: int, 
        chain: dict, 
        after_complete : coroutine,
        break_with_command : bool = False):

        """
        target_id : int - telegram ID of the person who will answer the chain of questions
        chain : dict - questions chain, format: { question_key : question }, example: { 'name' : 'What is your name?' }
        after_complete : async coroutine with dict arg, example: async some_function(answers : list)

        !WARNING! this object works only with text messages (aiogram restrictions)
        """

        self.target_id = target_id
        self.chain = chain

        self.questions = list(chain.values())
        self.quest_keys = list(chain.keys())

        self.current_quest_key = int()
        self.answers = dict()

        self.complete_coroutine = after_complete

        for question_key in self.quest_keys:
            setattr(self.AnswerModel, question_key,
                    self.AnswerModel.example_of_state_field)


    async def activate(self):
        await self.__ask(self.questions[0], self.quest_keys[0])


    async def __ask(self, question: str, field_name: str):
        await getattr(self.AnswerModel, field_name).set()
        await bot.send_message(self.target_id, question)

        self.current_quest_key += 1

        @dp.message_handler(state=getattr(self.AnswerModel, field_name))
        async def get_answer_of_my_dear_question(message: Message, state: FSMContext):
            self.answers[self.quest_keys[self.current_quest_key - 1]] = message.text

            async with state.proxy() as data:
                data[field_name] = message.text

            if self.current_quest_key == len(self.quest_keys):
                await state.finish()
                await self.complete_coroutine(self.answers)
                return

            await self.__ask(
                self.questions[self.current_quest_key],
                self.quest_keys[self.current_quest_key]
            )