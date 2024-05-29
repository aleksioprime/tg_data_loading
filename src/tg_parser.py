# класс, позволяющий нам подключаться к клиенту мессенджера и работать с ним
from telethon import TelegramClient
# функция, позволяющая работать с сообщениями в чате
from telethon.tl.functions.messages import GetDialogsRequest
# конструктор для работы с InputPeer, который передаётся в качестве аргумента в GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
# метод, позволяющий получить сообщения пользователей из чата и работать с ним
from telethon.tl.functions.messages import GetHistoryRequest
# специальный тип, определяющий объекты типа «канал/чат», с помощью которого можно обратиться к нужному каналу для парсинга сообщений
from telethon.tl.types import PeerChannel

import csv
import re
import os
import asyncio
from tqdm import tqdm

from config.logger import logger
from config.tg_settings import CSV_FILENAME
from src.utils import find_user


class TelegramParser:
    def __init__(self, phone, api_id, api_hash):
        logger.info("Инициализация клиента Telegram...")
        self.client = TelegramClient('anon', api_id, api_hash)
        self.phone = phone
        self.chats = []
        self.groups = []

    async def start(self):
        await self.client.start(self.phone)

    async def load_dialogs(self, size_chats=200):
        logger.info("Загрузка диалогов...")
        result = await self.client(GetDialogsRequest(
            offset_date=None,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=size_chats,
            hash=0
        ))
        self.chats.extend(result.chats)
        for chat in self.chats:
            try:
                if chat.megagroup:
                    self.groups.append(chat)
            except AttributeError:
                continue
        logger.info("Диалоги загружены")

    def choose_group(self):
        logger.info("Выбор группы...")
        if not self.groups:
            logger.warning("Группы не найдены")
            return None
        print("Группы:")
        for i, group in enumerate(self.groups):
            print(f"{i + 1} - {group.title}")
        print("0 - Выход")
        g_index = input("Введите номер группы: ")
        if g_index.isdigit() and g_index != '0':
            return self.groups[int(g_index) - 1]

    async def get_all_participants(self, target_group):
        logger.info(f"Получение участников для группы: {target_group.title}")
        logger.info(f"Получение участников группы: {target_group.title}")
        participants = await self.client.get_participants(target_group)
        logger.info(f"Количество участников получено: {len(participants)}")
        return participants

    async def get_messages(self, target_group, limit=100, total_count_limit=0):
        logger.info(f"Получение сообщений в группе: {target_group.title}")
        all_messages = []
        offset_id = 0
        total_messages = 0
        bar_format = "Загружено {n_fmt} сообщений | Прошло времени: {elapsed}"
        with tqdm(desc="Загрузка сообщений", bar_format=bar_format) as pbar:
            while True:
                history = await self.client(GetHistoryRequest(
                    peer=target_group,
                    offset_id=offset_id,
                    offset_date=None,
                    add_offset=0,
                    limit=limit,
                    max_id=0,
                    min_id=0,
                    hash=0
                ))
                if not history.messages:
                    break
                messages = history.messages
                for message in messages:
                    all_messages.append(message.to_dict())
                    pbar.update(1)
                offset_id = messages[-1].id
                total_messages += len(messages)
                if total_count_limit != 0 and total_messages >= total_count_limit:
                    break
                await asyncio.sleep(1)
        logger.info("Сообщения загружены")
        return all_messages

    async def save_to_csv(self, messages, target_group, filename=CSV_FILENAME):
        participants = await self.get_all_participants(target_group)
        if not participants:
            logger.warning("Не удалось получить участников группы")
            return None
        logger.info(f"Сохранение в файл export/{filename}...")
        path = os.path.join("export", filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="UTF-8") as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            writer.writerow(["user_id", "username", "fullname", "date", "message"])
            for message in messages:
                name_user = {}
                if 'from_id' in message and message['from_id'] is not None and 'user_id' in message['from_id']:
                    id_user = message['from_id']['user_id']
                    name_user = find_user(participants, id_user)
                else:
                    id_user = None
                if 'message' in message:
                    message_user = re.sub('[\t\r\n]', ' ', message['message'])
                else:
                    message_user = ''
                if message_user:
                    writer.writerow([id_user, name_user.get("username", ''), name_user.get("fullname", ''), message["date"], message_user])
        logger.info(f"Данные сохранены в {path}")
        return path