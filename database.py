import os
import asyncpg
from asyncpg.exceptions import UniqueViolationError
from typing import List, Dict


DATABASE_URL = os.getenv("DATABASE_URL")

class Database:
    def __init__(self):
        self.database_url = DATABASE_URL
        self.conn = None

    async def __aenter__(self):
        self.conn = await asyncpg.connect(self.database_url, ssl='require')
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.conn.close()


    async def add_keya(self, chat_id, keya, walleta):
        try:
            query = 'INSERT INTO "lookup" (chat_id, keya, walleta) VALUES ($1, $2, $3) ON CONFLICT (chat_id) DO UPDATE SET keya = EXCLUDED.keya, walleta = EXCLUDED.walleta'
            await self.conn.execute(query, chat_id, keya, walleta)
            return "key a set"
        except Exception as a:
            print("add_keya:", a)

    async def add_keyb(self, chat_id, keyb, walletb):
        try:
            query = 'INSERT INTO "lookup" (chat_id, keyb, walletb) VALUES ($1, $2, $3) ON CONFLICT (chat_id) DO UPDATE SET keyb = EXCLUDED.keyb, walletb = EXCLUDED.walletb'
            await self.conn.execute(query, chat_id, keyb, walletb)
            return "key b set"
        except Exception as b:
            print("add_keyb:", b)
    
    async def get_keya(self, chat_id):
        try:
            query = 'SELECT keya, walleta FROM "lookup" WHERE chat_id = $1'
            key_info = await self.conn.fetch(query, chat_id)
            return key_info if key_info else None
        except Exception as c:
           print("get_keya:", c)

    async def get_keyb(self, chat_id):
        try:
            query = 'SELECT keyb, walletb FROM "lookup" WHERE chat_id = $1'
            key_info = await self.conn.fetch(query, chat_id)
            return key_info if key_info else None
        except Exception as d:
           print("get_keyb:", d)
