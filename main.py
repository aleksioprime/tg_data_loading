import asyncio
from src.tg_parser import TelegramParser
from config.logger import logger
from config.tg_settings import API_ID, API_HASH, PHONE

async def main():
    parser = TelegramParser(PHONE, API_ID, API_HASH)
    await parser.start()
    await parser.load_dialogs()
    target_group = parser.choose_group()
    if target_group:
        messages =  await parser.get_messages(target_group)
        path = await parser.save_to_csv(messages, target_group, filename='messages.csv')
        print(f"Загрузка сообщений из группы {target_group.title} в файл {path} успешно выполнена!")

if __name__ == "__main__":
    asyncio.run(main())