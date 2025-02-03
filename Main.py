from Frontend.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    SetMicrophoneStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    AnswerModifier,
    QueryModifier,
    GetAssistantStatus,
    GetMicrophoneStatus
)

from Backend.Model import FirstLayerDMM
from Backend.RealTimeSearchEngine import RealtimeSearchEngine
from Backend. Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TTS import TextToSpeech
from dotenv import load_dotenv
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os

load_dotenv()

AssistantName = os.getenv("Assistantname")
Username = os.getenv("Username")
default_message = f'''{Username} : Hello {AssistantName}, How are you?{AssistantName} : Welcome {Username}. I'm doing well. How may I help you ?'''
subprocess = []
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

def ShowDefaultChatIfNoChats():
    File = open(r"Data\ChatLog.json", "r", encoding="utf-8")
    if len(File.read())<5:
        with open(TempDirectoryPath("Database.data"), "w", encoding="utf-8") as file:
            file.write("")
        with open(TempDirectoryPath("Responces.data"), "w", encoding="utf-8") as file:
            file.write(default_message)

def ReadChatLogJson():
    with open(r"Data\ChatLog.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def ChatLogIntegration():
    json_data = ReadChatLogJson() 
    formatted_chatlog = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"{Username}: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"{AssistantName}: {entry['content']}\n"
    formatted_chatlog = formatted_chatlog.replace("User", Username + " " )
    formatted_chatlog = formatted_chatlog.replace("Assistant", AssistantName + " " )
    
    with open (TempDirectoryPath("Database.data"), "w", encoding="utf-8") as file:
        file.write(AnswerModifier(formatted_chatlog))
        
def ShowChatsOnGUI():
    File = open (TempDirectoryPath("Database.data"), "r", encoding="utf-8")
    Data = File.read()
    if len(str(Data)) > 0:
        lines = Data.split("\n")
        results = "\n".join(lines)
        File.close()
        File = open(TempDirectoryPath("Responces.data"), "w", encoding="utf-8")
        File.write(results)
        File.close()
        
def InitialExecution():
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsOnGUI()
    
InitialExecution()

def MainExecution():
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""
    
    SetAssistantStatus("Listening...")
    Query = SpeechRecognition()
    ShowTextToScreen(f"{Username}:{Query}")
    SetAssistantStatus("Thinking...")
    Decision = FirstLayerDMM(Query)
    
    print("")
    print(f"Decision: {Decision}")
    print("")
    
    G = any([i for i in Decision if i.startswith("general")])
    R = any([i for i in Decision if i.startswith("realtime")])
    
    Merged_query = "and".join(
        [" ".join(i.split()[1: ]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
    )
    
    for queries in Decision:
        if "generate" in queries:
            ImageGenerationQuery = queries.split("generate")[1].strip()
            ImageExecution = True
        
    for queries in Decision:
        if TaskExecution == False:
            if any(queries.startswith(func) for func in Functions):
                run(Automation(list(Decision)))
                TaskExecution = True
                
    if ImageExecution == True:
        with open(r"Frontend\Files\ImageGeneration.data", "w") as file:
            file.write(f"{ImageGenerationQuery}, True")
                
                   
        try:
            p1 = subprocess.Popen(['python', r"Backend\ImageGeneration.py"],stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin= subprocess.PIPE, shell=False)
            subprocess.append(p1)
        except Exception as e:
            print(f"Error starting ImageGeneration.py{e}")
            
    if G and R or R:
        SetAssistantStatus("Searching....")
        Answer = RealtimeSearchEngine(QueryModifier(Merged_query))
        ShowTextToScreen(f"{AssistantName}:{Answer}")
        SetAssistantStatus("Answering....")
        TextToSpeech(Answer)
        return True
            
    else :
        for Queries in Decision:
            if "general" in Queries:
                SetAssistantStatus("Thinking....")
                QueryFinal = Queries.replace("general ", "")
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{AssistantName}:{Answer}")
                SetAssistantStatus("Answering....")
                TextToSpeech(Answer)
                return True
            elif "realtime" in Queries:
                SetAssistantStatus("Searching....")
                QueryFinal = Queries.replace("realtime ", "")
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{AssistantName}:{Answer}")
                SetAssistantStatus("Answering....")
                TextToSpeech(Answer)
                return True
            elif "exit" in Queries:
                QueryFinal = "Okay, Bye !"
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen = (f"{AssistantName}: {Answer}")
                SetAssistantStatus("Answering....")
                TextToSpeech(Answer)
                SetAssistantStatus("Answering...")
                os._exit(1)
                
def FirstThread():
    
    while True:
        CurrentStatus = GetMicrophoneStatus()
        
        if CurrentStatus == "True":
            MainExecution()
            
        else:
            AIstatus = GetAssistantStatus()
            
            if "Available" in AIstatus:
                sleep(0.1) 
            else:
                SetAssistantStatus("Available...")
                
def SecondThread():
    GraphicalUserInterface()
    
    
if __name__ == "__main__":
    thread2 = threading.Thread(target=FirstThread, daemon=True)
    thread2.start()
    SecondThread()
               