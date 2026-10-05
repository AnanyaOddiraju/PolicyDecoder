Chatbot for Multimodal RAG

ARCHITECTURE
                 USER QUERY
                     │
                     ▼
              Query understanding
                     │
                     ▼
             Entity/topic detection
                     │
                     ▼
              Semantic retrieval
                   Qdrant
                     │
                     ▼
             Relevant topic IDs
                     │
                     ▼
             Relationship expansion
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
        Text       Tables      Images
          │          │          │
          └──────────┼──────────┘
                     ▼
               Context builder
                     │
                     ▼
                    LLM
1) First create a groq acccount, get PAT
2) Create hugging face account and get PAT
3) Create a git repo and pull the code and update it and push to github
4)Push to hugging face using - git push space main
Linked huggingface and github code using :
git remote set-url space https://hugging face id:hugging_face_token@huggingface.co/spaces/spaceName

Merge the file contents if any merge issues occur

then run git push space main 

sequence while setting up for first time,
1. git clone repo_https/ssh link
2. get remote add space https://hfid:hf token@huggingface.co/spaces/hfid/spacename
3. git config pull.rebase false #pull hf files to avoid conflict
4. git pull space main --allow-unrelated-histories #pull hf files to avoid conflict
5. git add . # if readme conflicts occur merge the contents in vscode
6. git commit -m "message"  

After set up is done, sequence for everyday routine,
1. git add .
2. git commit -m "msg"
3. git push origin main
4. git push space main

Process
- python -m venv.venv
- .\.venv\Scripts\activate or  .\.venv\Scripts\Activate.ps1
- created project structure for pdf, docx, txt in mind (embeddings, chubking, pipeline etc fokders in src)
- pip install -r requirements.txt 
- Added loader, document_extractor, text_chunker, test_text_chunker
- pytest -q -s tests/unit/test_text_chunker.py
- python -m pytest -q -s path
- conda deactivate
- .\.venv\Scripts\python.exe -m pip install -U google-genai # to download new packages

