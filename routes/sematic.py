import asyncio
from semantic_kernel import Kernel
from service_settings import ServiceSettings
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.functions import KernelArguments
import pandas as pd
import re

# Ensure .env file is correctly configured with Azure details

# Asynchronous function to get recipe description
async def return_desc(re: str):
    try:
        # Initialize Kernel and configure Azure OpenAI settings
        kernel = Kernel()
        kernel.add_service(AzureChatCompletion(service_id="default", env_file_path='routes/.env'))
        
        # Load plugin
        plugin = kernel.add_plugin(parent_directory="routes/", plugin_name="FlugIn")
        desc_function = plugin["desc"]
        
        # Invoke plugin with the input
        function_result = await kernel.invoke(desc_function, KernelArguments(input=re))
        print(function_result)
        print(str(function_result))
        return str(function_result)
    
    except Exception as e:
        print(f"Error in return_desc: {e}")
        return "Description not available."

# Function to call asynchronous `return_desc`
def get_recipe_description(recipe_text: str):
    return asyncio.run(return_desc(recipe_text))

# Example to demonstrate how to get recipe details
def recipe_dict(li: list, item: str):
    li = li[0]
    re_dict = {}
    item = '-'.join(item.split(','))
    li_re = []
    for i in li:
        dt = {}
        name = i.replace('Recipe', '').replace('-', '')
        cleaned_name = re.sub(r"\(.*?\)", "", name).strip()
        dt['name'] = cleaned_name
        dt['description'] = get_recipe_description(i)
        dt['tags'] = ''.join(df[df['RecipeName'] == i]['Vegetables']).split(',')
        dt['calories'] = list(df[df['RecipeName'] == i]['TotalTimeInMins'])[0]
        dt['cuisine'] = list(df[df['RecipeName'] == i]['Cuisine'])[0]
        li_re.append(dt)
    re_dict[item] = li_re
    return re_dict


# Load your recipe data
df = pd.read_csv('data/modified_final.csv')

# Example input
recipe_text = [['Rase Wale Aloo Recipe (Boiled Potato in Tangy Tomato Sauce)', 
                'Chotti Aloor Dum Recipe - Baby Potatoes In Tomato Gravy', 
                'Sali Par Eedu Recipe - Parsi Breakfast Eggs On Fried Potato']]

# Generate descriptions
description = recipe_dict(recipe_text, 'tomato,potato')
print(description)
