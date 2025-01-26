from __future__ import annotations
from dotenv import load_dotenv
import os
from typing import Final


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


#database giveaway config

HOST: Final[str] = 'https://waayercglkxbowvbwwho.supabase.co'
PASSWORD:Final[str] = 'Adonis64@Adonis64'
NAME: Final[str] = 'postgres'
PORT: Final[str] = 5432
USER: Final[str] = 'postgres'