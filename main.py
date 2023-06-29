from aiogram.utils import executor

from utils import startup

from controller import dp


import handlers
executor.start_polling(dp, skip_updates=True, on_startup=startup)