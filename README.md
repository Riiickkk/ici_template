# Talk-To-Cashier


## Project Description

The project Talk-to-Cashier aims to develop an AI-powered virtual cashier system designed to assist customers in ordering beverages at drink shops. The motivation behind this project stems from four common issues observed in traditional human-operated ordering and cashier processes: excessive workload on cashiers during peak hours, potential hygiene concerns when staff are required to handle both cashiering and drink preparation simultaneously, a high rate of human error, and a heavy dependence on manual labor in existing ordering systems.

By integrating speech recognition,  large language models, and Retrieval-Augmented Generation (RAG) technologies, we built an AI cashier system capable of natural conversational interaction. The objective is to enable the AI cashier to receive and process verbal orders through speech recognition, accurately calculate the total amount based on selected items, and facilitate the checkout process via integrated payment functionalities. This approach aims to reduce labor demands, improve operational efficiency, and ensure a smooth and consistent customer experience.

For model training and testing, we selected the beverage brand “De Zheng” (得正) as our data source. The primary reason for choosing this brand lies in its relatively streamlined menu, which facilitates efficient and precise model training within the constraints of our limited resources and technical capacity, while also allowing us to focus on optimizing semantic understanding and menu structuring.

During development, we encountered several challenges, including training and deploying the RAG model in real-time interactive settings, building a structured menu database, and addressing information loss due to errors in speech recognition. We also placed particular emphasis on interface optimization and designed a voice-based interaction interface to enhance the system’s user-friendliness.

Looking forward, in response to an increasingly globalized society, we aim to expand the system’s multilingual support, incorporate more diverse ordering scenarios (e.g., dine-in vs. takeout options), further enhance the AI's semantic understanding and recommendation capabilities, and explore the feasibility of integration with more chain stores.

## How to Install and Run the Project

> The following instructions target **Windows 10/11 + Miniconda** because that is where most user mistakes occur.  
> macOS / Linux users can follow the **same steps**—just replace the installer, paths, and shell syntax that differ on your platform.

---

### 0. Prerequisites

| Item                | Get it here                                                     | Notes                                                             |
|---------------------|-----------------------------------------------------------------|-------------------------------------------------------------------|
| Miniconda (≈ 60 MB) | <https://docs.anaconda.com/free/miniconda/index.html>           | Install in a **pure-English path** such as `C:\Miniconda3`.       |
| Git                 | <https://git-scm.com/downloads>                                | For `git clone` (you can also download ZIP manually).             |
| OpenAI API Key      | <https://platform.openai.com/account/api-keys>                 | Make sure the key is **active** and your account still has credits.|

> **Why pure-English paths?**  
> Non-ASCII folders like `桌面` or OneDrive sync paths frequently cause path-encoding or permission errors on Windows.

---

### 1. Clone the repository
git clone https://github.com/Riiickkk/ici_template.git

---

### 2. Open *Anaconda Prompt* and enter the correct sub-directory
cd C:\Projects\ici_template\Group_4_Talk-To-Cashier\notebooks

You should see `main.py`, `requirements.txt`, etc. in this folder.

---

### 3. Create + activate the Conda environment

conda create -n cashier_env python=3.9 -y

conda activate cashier_env

The prompt prefix should now read `(cashier_env)`.

---

### 4. Install dependencies
pip install -r requirements.txt

> **Common pitfall** Forgetting FFmpeg causes  
> `FileNotFoundError: [WinError 2] The system cannot find the file specified`  
> when recording audio.

---

### 5. Set your OpenAI API key

#### 5.1 Recommended — set a **permanent** user variable

1. Search *Edit the system environment variables* → click **Environment Variables…**  
2. Under “User variables” click **New…**  
   * **Variable name:** `OPENAI_API_KEY`  
   * **Variable value:** `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx`  
     *No quotes, no trailing spaces.*
3. Click **OK** all the way out, then **close and reopen** Anaconda Prompt.

#### 5.2 Temporary — set for the current terminal only
$env:OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"

> **Top 3 mistakes**  
> 1. wrapping the key in quotes *inside* the env-var dialog → authentication fails  
> 2. leaving a space before/after the key → authentication fails  
> 3. using `set` in PowerShell (that’s CMD syntax) → variable isn’t exported

---

### 6. Run the app
python main.py

Successful startup prints e.g.:

Running on local URL: http://127.0.0.1:7860

Running on public URL: https://abcd1234ef56.gradio.live

1. Open **http://127.0.0.1:7860** in your browser.  
2. **Keep** the Anaconda Prompt window open – it’s your server.  
3. The public URL is for quick external demos (expires in ~72 h).

---

### 7. Quick-start script (copy-paste)
:: One-time setup

conda create -n cashier_env python=3.9 -y

conda activate cashier_env

pip install -r requirements.txt

conda install -c conda-forge ffmpeg -y

:: Daily usage

conda activate cashier_env

cd C:\Projects\ici_template\Group_4_Talk-To-Cashier\notebooks

python main.py

---

### 8. Troubleshooting Table

| Message / Symptom                                            | Likely Cause                                    | Fix |
|--------------------------------------------------------------|-------------------------------------------------|-----|
| `The api_key client option must be set…`                     | `OPENAI_API_KEY` missing / misspelled           | Re-set env-var, restart terminal |
| `FileNotFoundError: [WinError 2]` when recording             | FFmpeg not installed / not in PATH              | `conda install -c conda-forge ffmpeg -y` |
| `OMP: Error #15: Initializing libiomp5md.dll…`               | Intel OpenMP DLL conflict                       | `setx KMP_DUPLICATE_LIB_OK True` or set in code |
| Gradio shows **Connection errored out.** after recording     | Old Gradio / gradio_client bug                  | `pip install -U gradio gradio_client` |
| Using `set OPENAI_API_KEY=` in PowerShell has no effect      | CMD syntax in PowerShell                        | Use `$env:OPENAI_API_KEY="..."` |

---

### 9. Safety notes

* **Never** commit your API key to GitHub.  
* Consider adding `.env` to `.gitignore` if you use dot-env files.  
* Monitor your [OpenAI usage dashboard](https://platform.openai.com/account/usage) to avoid unexpected charges.

---

You’re all set — enjoy talking to your cashier bot! If you hit an unlisted issue, open an **Issue** with:

1. Full terminal error log  
2. OS + Python + Conda versions  
3. Exact steps to reproduce

## File Structure

> A concise overview of the key folders and files used at runtime.  
> Generic items such as `.gitignore`, licence files, and screenshots are omitted for clarity.

```
ici_template/
└── Group_4_Talk-To-Cashier/
    ├── data/                     # ← Knowledge base (structured + docs)
    │   ├── cashier.csv           #   SOP / FAQ for cashiers
    │   └── menu.pdf              #   Restaurant menu used for Q&A
    │
    ├── notebooks/                # ← All source code lives here
    │   ├── main.py               # Entry point; launches Gradio UI
    │   ├── audio_service.py      # Records mic, calls Whisper STT
    │   ├── llm_service.py        # Packs user text + context, calls OpenAI Chat API
    │   ├── vector_db_service.py  # Builds / queries ChromaDB
    │   ├── requirements.txt      # Python dependency list (pip install -r)
    │   └── .env.example          # Sample env-var file (copy → .env, add OPENAI_API_KEY)
    │
    └── README.md                 # ← Top-level project guide
```

### Module Responsibilities & Dependencies

| File / Dir                  | Purpose                                                                                     | Consumed / Called by            |
|-----------------------------|---------------------------------------------------------------------------------------------|---------------------------------|
| **`main.py`**              | 1️. Load vector DB&nbsp;·&nbsp;2️. Start Gradio UI&nbsp;·&nbsp;3️. Orchestrate the three services | imports the `*_service.py` files|
| **`audio_service.py`**     | Record microphone audio → `ffmpeg` → Whisper speech-to-text                                  | Returns text to `llm_service.py`|
| **`vector_db_service.py`** | Read **data/** → split → embed → store vectors; provides semantic search                     | Called by `llm_service.py`      |
| **`llm_service.py`**       | Combine *question + context* → OpenAI Chat API → return answer                               | Called by `main.py`             |
| **`data/`**                | Holds the `.csv` / `.pdf` knowledge-base files                                               | Loaded at startup               |
| **`requirements.txt`**     | Python dependency list (`pip install -r`)                                                    | —                               |
| **`.env.example`** | Example env-var file; copy to `.env` or set as system environment variable | — |


## Analysis

[Describe your analysis methods and include any visualizations or graphics that you used to present your findings. Explain the insights that you gained from your analysis and how they relate to your research question or problem statement.]

## Results

[Provide a summary of your findings and conclusions, including any recommendations or implications for future research. Be sure to explain how your results address your research question or problem statement.]

## Include Credits
This project was collaboratively completed by the following team members. We sincerely appreciate everyone’s dedication and contribution:

Hsin-Kai Hsu (Kevin),
Yan-Ray Liu (Rick),
Shih-Yi Wang (Chloe),
Ching-Fu Yang (Leo),
Hsu-He Chiu (Robert).
We would like to express our special thanks to Professor Pien Chung-pei of National Chengchi University for his professional guidance and valuable teaching throughout the Introduction to AI course.

During the design and implementation of this project, we referred to the following course modules as technical and conceptual foundations:
AIGC and ChatGPT’s Advanced Application: Fine-tune,
AIGC and ChatGPT’s Advanced Application: RAG.
These resources significantly deepened our understanding of generative AI, including model fine-tuning and retrieval-augmented generation (RAG), and contributed greatly to the realization of this project.

## Add a License
MIT License

Copyright (c) 2025 Kevin Hsu, Rick Liu, Chloe Wang, Leo Yang, Robert Chiu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell    
copies of the Software, and to permit persons to whom the Software is        
furnished to do so, subject to the following conditions:                     

The above copyright notice and this permission notice shall be included in   
all copies or substantial portions of the Software.                          

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR   
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,     
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER       
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING      
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
IN THE SOFTWARE.

## References

Drink menu data was sourced from the official Facebook post by DeZheng OOLONG TEA PROJECT:
Menu 2025 - Facebook. 
This information was used solely for academic and experimental purposes.

Large language model integration was powered by OpenAI's GPT-4o API and the LangChain framework.

Document loading and vector search were implemented using langchain-community loaders and Chroma vector database.

Audio transcription was handled using OpenAI Whisper; text-to-speech (TTS) was implemented using gTTS (Google Text-to-Speech).

All training, implementation, and testing were conducted in a non-commercial, educational setting as part of the Introduction to AI course at National Chengchi University.
