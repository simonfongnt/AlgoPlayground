import logging
import telegram
from telegram.error import NetworkError, Unauthorized
import time
from threading import Thread
import datetime
import pandas as pd
import re
import sys


# Telegram API
class tgApi(Thread):
    
    def __init__(
            self, 
            thQueue, 
            mpQueue,
            token, 
            botname, 
            authgroup, 
            itag, 
            otag,
            suicidable = False,
            ):
        # super().__init__()
        Thread      .__init__(self)
        self.thQueue    = thQueue        
        self.mpQueue    = mpQueue
        self.update_id  = None
        self.authgroup  = authgroup
        self.TOKEN      = token 
        self.botname    = botname
        # # Telegram Bot Authorization Token
        # self.bot        = telegram.Bot(self.TOKEN)
        self.bot        = None
        # i/o tag
        self.itag       = itag
        self.otag       = otag
        self.suicidable = suicidable
    
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        self.lmtFailsafe    = 10
        self.tsFailsafe     = time.time() + self.lmtFailsafe
        self.thID           = self.itag + '-' + str(int(self.tsFailsafe))
        
        self.strMaxLen      = 4096
        
    def listen(self):
        """Echo the message the user sent."""
#        global update_id
        # Request updates after the last update_id
        for update in self.bot.get_updates(offset = self.update_id, timeout=10):
            self.update_id = update.update_id + 1
            try:
                if update.message.chat.id == self.authgroup:
                    self.chat_id = update.message.chat.id
                    input_msg = update.message.text
                    try:                        
                        # entities exists and type is bot_command 
                        if input_msg.endswith(self.botname):                        # check if the text ends with bot's name
                            input_msg = input_msg[:-len(self.botname)]              # /command@constituentsBot -> /command
                        if update.message.entities and update.message.entities[0].type == 'bot_command':
                            input_msg = input_msg[1:]                               # /command -> command
                        input_msg = re.split("[, \-!?:_]+", input_msg)
                            
                        self.thQueue[self.otag].put(input_msg)
                        self.thQueue[self.otag].join()  # blocks until consumer calls task_done()
                    except Exception as e:
                        print (
                                self.itag, 
                                sys._getframe().f_code.co_name, 
                                'invalid command: ', 
                                e,
                                )
            except Exception as e:
                print (
                        self.itag, 
                        sys._getframe().f_code.co_name, 
                        e,
                        )
                time.sleep(1)
    
    def cycle(self):
        try:
            # Telegram Bot Authorization Token
            if not self.bot:
                self.bot = telegram.Bot(self.TOKEN)
                # get the first pending update_id, this is so we can skip over it in case
                # we get an "Unauthorized" exception.
                try:
                    self.update_id = self.bot.get_updates()[0].update_id
                except IndexError:
                    self.update_id = None
            else:
                self.listen()
        except NetworkError:
            time.sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            self.update_id += 1
        except Exception as e:
            print (
                    self.itag, 
                    sys._getframe().f_code.co_name, 
                    e,
                    )
            time.sleep(1)
        
    def run(self):
        """
        Run is the main-function in the new thread. Here we overwrite run
        inherited from threading.Thread.
        """
        self.status = True
        while self.status:
            if (    # can be suicided
                    self.suicidable
                    # Failsafe Shutdown
                and time.time() > self.tsFailsafe + self.lmtFailsafe                
                    ):
                print(self.thID, 'BREAK!')
                break  
#            print ('telegram running...')                
            if (
                    self.thQueue[self.itag].empty()
                and self.mpQueue[self.itag].empty()
                    ):
#                print ('telegram queue is empty...')
                self.cycle()
                time.sleep(1)                           # optional heartbeat
                
            elif not self.thQueue[self.itag].empty():   
                # print ('telegram queue has sth...')
                self.thPrompt()
                self.thQueue[self.itag].task_done()  # unblocks prompter  
            elif not self.mpQueue[self.itag].empty():   
                # print ('telegram queue has sth...')
                self.mpPrompt()
                self.mpQueue[self.itag].task_done()  # unblocks prompter   
#                print ('telegram task_done')
        raise SystemExit
                
    def stop(self):
        self.status = False
        Thread.join(self, None)

    def divideCmds(
            self,
            cmds,
            ):
        pass

    def send(
            self,
            cmds,
            ):
        if (
                '.png' in cmds
            or  '.jpg' in cmds
                ):
            self.bot.send_photo(chat_id = self.authgroup, photo=open(cmds, 'rb'), timeout=100)
        else:
            idx = len(cmds)
            # divide msg based on string limit if possible
            while(len(cmds) >= self.strMaxLen):
                idx     = self.strMaxLen
                # search for newline
                while cmds[idx] != '\n':
                    idx = idx - 1                        
                self.bot.send_message(chat_id = self.authgroup, text = cmds[:idx])
                cmds = cmds[idx:]                    
            self.bot.send_message(chat_id = self.authgroup, text = cmds[:idx])

    def thPrompt(self):
        try:
            while not self.thQueue[self.itag].empty():
                cmds = self.thQueue[self.itag].get()
#                self.bot.send_message(chat_id = self.chat_id, text = cmds)
                # print (cmds)
                self.send(cmds)
        except Exception as e:
            print('Command `{cmds}` is unknown: ', e)
            
    def mpPrompt(self):
        try:
            while not self.mpQueue[self.itag].empty():
                cmds = self.mpQueue[self.itag].get()
#                self.bot.send_message(chat_id = self.chat_id, text = cmds)
                # print (cmds)
                self.send(cmds)
                
        except Exception as e:
            print('Command `{cmds}` is unknown: ', e)
            
    # Report Params
    def set(self, name, val):
        if name == 'accounts':
            self.accounts   = val
        elif name == 'tsFailsafe': 
            self.tsFailsafe = val
        return None
#if __name__ == '__main__':
#    main()
    
