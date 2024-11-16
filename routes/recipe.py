import asyncio
from semantic_kernel import Kernel
from routes.service_settings import ServiceSettings
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.functions import KernelArguments
import pandas as pd
import re
from datetime import datetime
import ast


async def return_desc(re: str):
    kernel = Kernel()
    service_settings = ServiceSettings.create()
    kernel.remove_all_services()
    kernel.add_service(AzureChatCompletion(service_id="default", env_file_path='routes/turbo.env'))
    plugin = kernel.add_plugin(parent_directory="routes/", plugin_name="FlugIn")
    desc_function = plugin["desc"]
    description = await kernel.invoke(desc_function, KernelArguments(input=re))
    return description

async def get_recipe_description(recipe_text):
    description = await return_desc(recipe_text)
    return str(description)

async def return_ins(re: str):
    kernel = Kernel()
    service_settings = ServiceSettings.create()
    kernel.remove_all_services()
    kernel.add_service(AzureChatCompletion(service_id="default", env_file_path='routes/turbo.env'))
    plugin = kernel.add_plugin(parent_directory="routes/", plugin_name="FlugIn")
    desc_function = plugin["recipie"]
    description = await kernel.invoke(desc_function, KernelArguments(input=re))
    return description

async def get_recipe_instruction(recipe_text):
    df = pd.read_csv('data/modified_final.csv')
    ins = df[df['RecipeName']==recipe_text]['Instructions']
    description = await return_ins(ins)
    abs = {}
    abs['instructions']=str(description)
    abs['serve'] = list(df[df['RecipeName']==recipe_text]['Servings'])[0]
    abs['preptime'] = list(df[df['RecipeName']==recipe_text]['TotalTimeInMins'])[0]
    abs['ingredients'] = list(df[df['RecipeName']==recipe_text]['Ingredients'])[0]
    abs['diet'] = list(df[df['RecipeName']==recipe_text]['Diet'])[0]


    return abs


async def recipe_dict(li:str,item:str):
    li = li[0]
    df = pd.read_csv('data/modified_final.csv')
    re_dict = {}
    item = '-'.join(item.split(','))
    li_re = []
    print("strt ",li)
    desk = await get_recipe_description(li)
    print(desk)
    if desk == 'No recipes provided':
        return desk
    desk = ast.literal_eval(desk)
    print(desk)
    for i,j in zip(li,desk):
        dt = {}
        print(j)
        name = i.split("Recipe")[0].strip()
        name = name.replace('Recipe','')
        name = name.replace('-','')
        cleaned_name = re.sub(r"\(.*?\)", "", name).strip()
        dt['name'] = cleaned_name
        dt['description'] = j
        dt['main_name'] = i
        print("ajj",type(i))
        dt['tags'] = ''.join(df[df['RecipeName']==i]['Vegetables']).split(',')
        dt['calories']=list(df[df['RecipeName']==i]['TotalTimeInMins'])[0]
        dt['cuisine'] = list(df[df['RecipeName']==i]['Cuisine'])[0]
        li_re.append(dt)
    re_dict[item]=li_re
    return re_dict


start =  datetime.now()
print("start time : ",start)

# df = pd.read_csv('data/modified_final.csv')
# recipe_text =  [['Rase Wale Aloo Recipe (Boiled Potato in Tangy Tomato Sauce)', 'Chotti Aloor Dum Recipe - Baby Potatoes In Tomato Gravy', 'Sali Par Eedu Recipe - Parsi Breakfast Eggs On Fried Potato']]
# description = recipe_dict(recipe_text,'tomato,potato')
# print(description)
end = datetime.now()
print("end time : ",end)
