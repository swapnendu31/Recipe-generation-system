from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from routes.search import get_exact_recipes
from routes.recipe import get_recipe_description,get_recipe_instruction,recipe_dict
from routes.service_settings import ServiceSettings

app = FastAPI()

# Serving static files
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")

# Rendering HTML templates
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
# Example recipes data (just like in your JavaScript)
recipes = {
    'tomato': [{
        'name': 'Tomato Soup',
        'description': 'A warm soup made with fresh tomatoes.',
        'instructions': '1. Heat oil in a pan. 2. Add chopped tomatoes and cook until soft. 3. Blend the tomatoes and season with salt and pepper.',
        'tags': ['tomato', 'soup', 'vegetarian'],
        'calories': '128',
        'cuisine': 'north'
    }],
    'potato-tomato': [{
        'name': 'Mashed Potatoes',
        'description': 'Creamy mashed potatoes.',
        'instructions': '1. Boil potatoes until soft. 2. Mash with butter and cream.',
        'tags': ['potato', 'vegetarian'],
        'calories': '158',
        'cuisine': 'north'
    }],
    'carrot': [{
        'name': 'Carrot Cake',
        'description': 'A moist cake with grated carrots.',
        'instructions': '1. Mix grated carrots, flour, and sugar. 2. Add eggs and baking soda. 3. Bake at 350°F for 30 minutes.',
        'tags': ['carrot', 'cake'],
        'calories': '108',
        'cuisine': 'south'
    }]
}

@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

# New route to handle vegetable search
@app.get("/search/")
async def search_vegetable(query: str):
    veg = [query.split(',')]
    print(query)
    search_re = get_exact_recipes(veg)
    print(search_re)
    print("this is here : ", len(search_re))
    if len(search_re[0]) == 0:
        non = {'recipes' : []}
        return non
    dict_re = await recipe_dict(search_re,query)
    print(dict_re)


    print(query)
    vegetables = query.split(',')
    print(vegetables)
    matched_recipes = []
    for vegetable in vegetables:
        vegetable = vegetable.strip()
        print(vegetable)  # Clean up any extra spaces
        if vegetable in dict_re:
            matched_recipes.extend(dict_re[vegetable])
    return JSONResponse(content={"recipes": matched_recipes})



# Define a function to return recipe instructions by recipe name
@app.get("/return_inst/")
async def return_inst(recipe_name:str):
    print("as",recipe_name)
    instuctions = ''
    instuctions  = await get_recipe_instruction(recipe_name)
    print("iuns ",instuctions)
    # recipe = next((r for r in recipes if r["name"].lower() == recipe_name.lower()), None)
    
    if instuctions :
        return JSONResponse(content={"instructions": instuctions })
    else:
        return JSONResponse(content={"instructions": "No instructions found for this recipe."}, status_code=404)




