import ctypes
import json
import os
import logging
import pymem
import pymem.process

from colorama import Fore


class CSMemory:
    CACHE_DIRECTORY = os.path.expandvars(r'OffsetsData')
    CACHE_FILE = os.path.join(CACHE_DIRECTORY, 'offsets_cache.json')

    def __init__(self):
        offsets, client_data = self.fetch_offsets()

        self.pm = None
        self.client_base = None

        self.dwEntityList = 0
        self.dwLocalPlayerPawn = 0
        self.m_iHealth = 0
        self.m_iTeamNum = 0
        self.m_iIDEntIndex = 0
        self.m_iPosition = 0
        self.m_viewAngles = 0
        self.m_playerviewAngles = 0
        self.m_bHasMatchStarted = 0

        if not self.initialize_pymem():
            input(f"{Fore.RED}Press Enter to exit...")
            return
        if not self.get_client_module():
            input(f"{Fore.RED}Press Enter to exit...")
            return

    def get_client_module(self):
        client_module = pymem.process.module_from_name(self.pm.process_handle, "client.dll")
        if not client_module:
            logging.error(f"{Fore.RED}Could not find client.dll module.")
            return False
        self.client_base = client_module.lpBaseOfDll
        return True

    def initialize_pymem(self):
        try:
            self.pm = pymem.Pymem("cs2.exe")
        except pymem.exception.PymemError as e:
            logging.error(f"{Fore.RED}{e}")
            return False
        return True

    def fetch_offsets(self):
        # 获取缓存文件
        return None, None

    def getTeamFlag(self, address):
        return self.pm.read_int(address + self.m_iTeamNum)

    def getHealth(self, address):
        return self.pm.read_int(address + self.m_iHealth)

    def getPosition(self, address):
        return self.pm.read_float(address + self.m_iPosition), self.pm.read_float(address + self.m_iPosition + 4)

    def getViewAngles(self, address):
        return self.pm.read_float(address + self.m_viewAngles + 4)

    def get_entityByid(self, index):
        try:
            ent_list = self.pm.read_longlong(self.client_base + self.dwEntityList)
            ent_entry = self.pm.read_longlong(ent_list + 0x8 * (index >> 9) + 0x10)
            return self.pm.read_longlong(ent_entry + 120 * (index & 0x1FF))
        except Exception as e:
            logging.error(f"{Fore.RED}Error reading entity: {e}")
            return None
