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


@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

# New route to handle vegetable search
@app.get("/search/")
async def search_vegetable(query: str):
    
    veg = [query.split(',')]
    # print("que = ",query)
    search_re = get_exact_recipes(veg)
    # print("ser = ",search_re)
    # print("this is here : ", len(search_re))
    if len(search_re[0]) == 0:
        non = {'recipes' : []}
        return non
    dict_re = await recipe_dict(search_re,query)
    vegetables = query.split(',')
    print(dict_re)
    print(query.replace(',','-'))
    veg = query.split(',')
    print(len(veg))
    matched_recipes = []
    # for vegetable in vegetables:
    #     vegetable = vegetable.strip()
    #     print(vegetable) 
    #     if vegetable in dict_re:
    #         matched_recipes.extend(dict_re[vegetable])
    # print("\n\n ===",matched_recipes)

    if len(veg)>1:
        veg_len = '-'.join(veg)
        matched_recipes.extend(dict_re[query.replace(',','-')])
    else:
        matched_recipes.extend(dict_re[query])
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




