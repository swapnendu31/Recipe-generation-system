# Recipe Generation AI 🍲  
_A system to generate recipes based on available vegetables using a robust search engine._

## 📚 Overview  
Recipe Generation AI is a smart application designed to generate recipes using only the vegetables that are available to the user.  
It features a **robust search engine** built using a **bipartite graph** to match vegetables with recipes and utilizes **Microsoft Semantic Kernel** to deliver narrative-style instructions.  
The system is user-friendly, providing additional information like diet and cuisine etc and interactive UI components for a seamless experience.

### Key Features:  
- **Ingredient-Based Recipes**: Generates recipes based on vegetables detected by the user.  
- **Robust Search Engine**: Matches available vegetables to recipes using a bipartite graph.  
- **Narrative Instructions**: Transforms recipe steps into narrative-style descriptions using Semantic Kernel.  
- **Interactive UI**: Includes dynamic panels for recipe instructions and details.

---

## 👩‍💻 Team  
- **Swapnendu Let**  
  - _Role_: Backend Development and Deployment.  
  - _Contributions_:  
    - Developed the bipartite graph-based recipe matching system.  
    - Created the backend using FastAPI.  
    - Deployed the application on Heroku. 
    - Integrated Microsoft Semantic Kernel for narrative recipe descriptions.   

- **[Geetansh Upreti](https://github.com/GeetanshUpreti)**  
  - _Role_: Frontend and Data collection.  
  - _Contributions_:  
    - Designed and developed the interactive user interface.  
    - Collected, curated, and preprocessed vegetable and recipe datasets
    - Enhanced the system for improved user experience.

---

## 🚀 Deployment  
The application is live at: [Heroku Link](https://recipe-generation-system-c19e064afb24.herokuapp.com)

---

## 🛠️ Tech Stack  
- **Backend**: FastAPI, Python  
- **Frontend**: JavaScript, HTML, CSS  
- **Deployment**: Heroku  
- **AI Tools**: Microsoft Semantic Kernel, P   
- **Data Science Libraries**: Pandas, NumPy  
---

## 📂 Setup Instructions  

1. **Clone the repository**:  
   ```bash
   git clone https://github.com/your-repo/recipe-generation-ai.git
   cd recipe-generation-ai

2. **Install dependencies**: 
  ```bash
   pip install -r requirements.txt


3. **Run the server**:
  ```bash
   uvicorn main:app --reload
   ## Open http://127.0.0.1:8000 in your browser.

