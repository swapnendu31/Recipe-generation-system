let searchTags = [];
const searchInput = document.getElementById('tag-input');
const tagContainer = document.getElementById('tag-container');
const suggestionsContainer = document.getElementById('suggestions-container');
const availableTagsContainer = document.getElementById('available-tags');
const recipeList = document.getElementById('recipe-list');
const availableTags = [
    'amaranth', 'apple gourd', 'arugula', 'ash gourd', 'asparagus', 'baby corn', 'bamboo shoot', 'bean', 
    'beetroot', 'bitter gourd', 'bottle gourd', 'brinjal', 'broccoli', 'cabbage', 'capsicum', 'cape gooseberry', 
    'carrot', 'cassava', 'celery', 'chickpea', 'chives', 'cluster bean', 'coconut', 'colocasia', 'coriander leaf', 
    'cress', 'cucumber', 'curry leaf', 'dill', 'drumstick', 'elephant foot yam', 'endive', 'fava bean', 'fenugreek leaf', 
    'french bean', 'garlic', 'ginger', 'gooseberry', 'green chili', 'green onion', 'ivy gourd', 'jackfruit', 
    'jute flower', 'kale', 'kidney bean', 'lady finger', 'lemon', 'lettuce', 'little gourd', 'lotus root', 'mints', 
    'mushroom', 'mustard green', 'natal plum', 'olive', 'onion', 'parsnip', 'pea', 'plantain', 'pointed gourd', 
    'potato', 'pumpkin', 'radish', 'raw banana flower', 'raw mango', 'raw papaya', 'red chili', 'rhubarb', 'ridge gourd', 
    'runner bean', 'scallion', 'shallot', 'snake gourd', 'soya bean', 'spinach', 'spring onion', 'sponge gourd', 
    'sweet corn', 'sweet potato', 'tamarind', 'taro', 'tendli gourd', 'tomato', 'turnip', 'water chestnut', 'white brinjal', 
    'wild spinach', 'yam'
];

// Generate available tags from vegetable array
availableTags.forEach(tag => {
    const tagDiv = document.createElement('div');
    tagDiv.classList.add('available-tag');
    tagDiv.textContent = tag;
    tagDiv.onclick = () => addTag(tag);
    availableTagsContainer.appendChild(tagDiv);
});

function addTag(tag) {
    if (!searchTags.includes(tag)) {
        searchTags.push(tag);
        const tagElement = document.createElement('div');
        tagElement.classList.add('tag');
        tagElement.textContent = tag;
        const closeButton = document.createElement('span');
        closeButton.classList.add('close');
        closeButton.textContent = 'x';
        closeButton.onclick = () => removeTag(tag, tagElement);
        tagElement.appendChild(closeButton);
        tagContainer.appendChild(tagElement);
        searchInput.value = ''; // Clear the input after adding the tag
        suggestionsContainer.style.display = 'none'; // Hide the suggestions after adding the tag
        searchVegetable(searchTags.join(',')); // Search using the selected tags
    }
}

function removeTag(tag, tagElement) {
    searchTags = searchTags.filter(t => t !== tag);
    tagContainer.removeChild(tagElement);
    searchVegetable(searchTags.join(',')); // Update search when a tag is removed
}

function showSuggestions() {
    const inputText = searchInput.value.toLowerCase();
    if (inputText) {
        const filteredSuggestions = availableTags.filter(tag => tag.startsWith(inputText));
        suggestionsContainer.innerHTML = '';
        filteredSuggestions.forEach(tag => {
            const suggestionItem = document.createElement('div');
            suggestionItem.classList.add('suggestion-item');
            suggestionItem.textContent = tag;
            suggestionItem.onclick = () => addTag(tag);
            suggestionsContainer.appendChild(suggestionItem);
        });
        suggestionsContainer.style.display = 'block';
    } else {
        suggestionsContainer.style.display = 'none';
    }
}

// Fetch recipes based on the search tags
async function searchVegetable(query) {
    if (!query) {
        // Clear the recipe list if the query is empty
        recipeList.innerHTML = 'No recipes found. Please select a vegetable to search.';
        return;
    }

    try {
        // Fetch recipes based on the query
        const response = await fetch(`/search/?query=${query}`);
        const data = await response.json();

        // Display the fetched recipes
        displayRecipes(data.recipes);
    } catch (error) {
        console.error('Error fetching recipes:', error);
        recipeList.innerHTML = 'An error occurred while fetching recipes. Please try again later.';
    }
}

// Display the recipes on the front-end
// Display the recipes on the front-end
function displayRecipes(recipes) {
    console.log('Recipes:', typeof(recipes));  // Log the recipes to check the structure
    recipeList.innerHTML = ''; // Clear previous recipes
    if (recipes.length === 0) {
        recipeList.innerHTML = 'No recipes found for these vegetables.';
        return;
    }
    
    recipes.forEach(recipe => {
        const recipeItem = document.createElement('div');
        recipeItem.classList.add('recipe-item');
        console.log('log1 ',recipe)
        recipeItem.onclick = () => showRecipeInstructions(recipe);
        recipeItem.innerHTML = `
            <div id="item_name_box">
                <h3>${recipe.name}</h3>
                <p>${recipe.description}</p>
                <div class="tags">${recipe.tags.map(tag => `<span>${tag}</span>`).join('')}</div>
            </div>
            <div id="cal_box">
                <p><strong>Cuisine:</strong> ${recipe.cuisine}</p>
                <p><strong>Total Cooking Time :</strong> ${recipe.calories} Mins</p>
            </div>
        `;
        recipeList.appendChild(recipeItem);
    });
}


// Show the instructions for a recipe
async function showRecipeInstructions(recipe) {
    console.log('Fetching instructions for:', recipe.main_name);
    
    // Call the backend to fetch instructions
    const response = await fetch(`/return_inst/?recipe_name=${encodeURIComponent(recipe.main_name)}`);
    const data1 = await response.json();
    
    if (response.ok) {
        data = data1.instructions
        const instructions = data.instructions;
        const predtim = data.predtime
        document.getElementById('recipe-name').textContent = recipe.name;
        document.getElementById('preptime').innerHTML =`<strong>Cooking Duration :</strong> ${data.preptime} Mins`;
        document.getElementById('serve').innerHTML  = `<strong>Serves :</strong> ${data.serve}`;
        document.getElementById('diet').innerHTML  = `<strong>Diet Type :</strong> ${data.diet}`;
        document.getElementById('ingredients').innerHTML  = `<strong>Ingredients :</strong> ${data.ingredients}`;
        // Check if instructions are in the correct format and display them
        document.getElementById('recipe-instructions').innerHTML = `<br><strong>Instructions :</strong><br>${instructions.replace(/\n/g, '<br>')}`;
    } else {
        document.getElementById('recipe-name').textContent = 'Recipe not found';
        document.getElementById('recipe-instructions').textContent = 'No instructions available.';
    }
    
    // Show the instruction panel
    document.getElementById('instruction-panel').classList.add('active');
}

// Go back to the recipes list
function goBack() {
    document.getElementById('instruction-panel').classList.remove('active');
}


