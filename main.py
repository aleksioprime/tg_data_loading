from src.tg_parser import TelegramParser
from config.logger import logger
from config.tg_settings import API_ID, API_HASH, PHONE

def main():
    parser = TelegramParser(PHONE, API_ID, API_HASH)
    parser.load_dialogs()
    target_group = parser.choose_group()
    if target_group:
        messages = parser.get_messages(target_group)
        path = parser.save_to_csv(messages, target_group, filename='messages.csv')
        print(f"Загрузка сообщений из группы {target_group.title} в файл {path} успешно выполнена!")

if __name__ == "__main__":
    main()