import subprocess
import os

class LinuxTools:
    def __init__(self):
        pass

    def pskill(self, thread_name:str="")->None:
        """Kill thread by name"""
        if not thread_name: return 
        os.system(f'pkill -f {thread_name}')

