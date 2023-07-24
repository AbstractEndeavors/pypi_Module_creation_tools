import PySimpleGUI as sg
from abstract_utilities.class_utils import call_functions,process_args,get_fun,mk_fun
def get_gui_fun(name:str='',args:dict={}):
  return get_fun({"instance":sg,"name":name,"args":args})
def single_call(win):
  event, values = win.read()
  win.close()
  return values
def get_browser(type:str='Folder',text:str='',title:str='select Direcoty'):
  sg.theme('Dark Grey 13')
  
  window = get_gui_fun(name=f'Window',args={"title":f"{title}", "layout":[[get_gui_fun(name='Text',args={'text':text})],[sg.Input(), get_gui_fun(name=f'{type}Browse',args={})],[sg.OK(), sg.Cancel()]]})
  return single_call(window)['Browse']

