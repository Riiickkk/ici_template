# Talk-To-Cashier


## Project Description

Talk-to-Cashier is an AI-powered virtual cashier system designed to assist customers in ordering beverages at drink shops. By integrating speech recognition, large language models, and Retrieval-Augmented Generation (RAG), our system enables natural conversational ordering, accurate total calculation, and seamless payment processing. This approach reduces labor demands, improves operational efficiency, and delivers a consistent, user-friendly experience.

### Why we develop this project
- Address four common issues in traditional cashier systems:
  - Excessive workload on cashiers during peak hours  
  - Hygiene concerns when staff handle both cashiering and drink preparation  
  - High human error rates  
  - Heavy dependence on manual labor  
- Streamline ordering, improve efficiency, and ensure a consistent customer experience

### Core Technologies
- **Speech Recognition** to capture verbal orders in real time  
- **Large Language Models** for natural conversational interaction and intent understanding  
- **Retrieval-Augmented Generation (RAG)** to fetch precise menu and promotion details from a structured database  

### Key Features
- **Natural Conversational Interaction**: Fluid, human-like dialogues with customers  
- **Automated Order Processing**: Calculates totals and integrates with payment gateways  
- **Easy Content Updates**: Update menu items and promotions without redeploying code  
- **High Adaptability**: Rapid deployment across multiple store locations with minimal configuration  
- **Standardized Ordering & Recording**: Automatically logs every interaction for accuracy and analysis  
- **Multilingual Support**: Handles orders in different languages for a diverse customer base  

### Data Source & Model Training
- Selected the beverage brand **“De Zheng” (得正)** for its streamlined menu, enabling efficient training within resource constraints  
- Focused on optimizing semantic understanding and menu structuring for precise order handling  

### Development Challenges
- Real-time training and deployment of the **RAG model** in interactive settings  
- Building and maintaining a **structured menu database**  
- Mitigating response errors caused by **speech recognition inaccuracies**  
- Designing a **voice-based interaction interface** for enhanced user friendliness  

### Future Directions
- Expand **multilingual support** for a global customer base  
- Incorporate diverse ordering scenarios (e.g., dine-in vs. takeout)  
- Further enhance the AI’s **semantic understanding** and **recommendation capabilities**  
- Explore integration with chain-store systems  

---

## How to Install and Run the Project

> The following instructions target **Windows 10/11 + Miniconda** because that is where most user mistakes occur.  
> macOS / Linux users can follow the **same steps**—just replace the installer, paths, and shell syntax that differ on your platform.

---

### 0. Prerequisites

Before proceeding, ensure you have the following installed and configured:

| Item               | Download Link                                                      | Notes                                                                                |
|--------------------|--------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| **Miniconda**      | `https://docs.anaconda.com/free/miniconda/index.html`              | • Install into a folder with only ASCII characters (e.g., `C:\Miniconda3`)           |
| **Git**            | `https://git-scm.com/downloads`                                    | • Used for `git clone`                                                               |
| **OpenAI API Key** | `https://platform.openai.com/account/api-keys`                     | • Ensure your key is active and you have enough quota<br>• Store the key securely (never commit to source control) |

> **Why ASCII-only paths?**  
> On Windows, folders with non-ASCII characters (e.g., "Desktop" or OneDrive-synced folders) often cause path-encoding errors or permission issues, preventing the project from running correctly.

---

### 1. Clone the repository
Open Anaconda Prompt and run the following command to clone the original project:
```bash
git clone https://github.com/Riiickkk/ici_template.git
```
If you have forked the repository under your own account, replace the URL with your fork’s address, for example:
```bash
git clone https://github.com/<your-username>/ici_template.git
```
Tip: If you download the ZIP archive instead, extract it into a folder whose path contains only ASCII characters (e.g., C:\Projects\ici_template) to avoid any path-encoding issues.

---

### 2️. Open Anaconda Prompt

#### 2-1. Launch Anaconda Prompt
Press the Windows key, type **“Anaconda Prompt”**, and hit Enter. 
You should see a black window with the prompt starting with  **`(base)`**.  
> If you see `C:\>` without `(base)`, you are using the regular CMD. Please close it and reopen Anaconda Prompt.

#### 2-2. Change to the project directory
Type the following command in Anaconda Prompt to change to the correct folder:
```bash
cd C:\Projects\ici_template\Group_4_Talk-To-Cashier\notebooks
```
> You should see files like main.py, requirements.txt, etc. in this folder.

---

### 3. Create + activate the Conda environment
Type the following command in Anaconda Prompt:
```bash
conda create -n cashier_env python=3.9 -y

conda activate cashier_env
```
The prompt prefix should now read `(cashier_env)`.

---

### 4. Install dependencies
Type the following command in Anaconda Prompt:
```bash
pip install -r requirements.txt
```
---

### 5️. Set your OpenAI API key

#### 5.1. Set a **permanent** user variable (Recommended)
1. Search **"Edit the system environment variables"** → click **Environment Variables…**  
2. Under "User variables" click **New…**  
   * **Variable name:** `OPENAI_API_KEY`  
   * **Variable value:** `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx`  
     *No quotes, no trailing spaces.*
3. Click **OK** all the way out, then **close and reopen** your terminal.

#### 5.2. Set for the current terminal only (Temporary)

The syntax depends on which type of Anaconda terminal you're using:

**For Anaconda Prompt (CMD-based) - most common:**
```
set OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**For Anaconda PowerShell Prompt:**
```
$env:OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

> **How to identify which you're using:**  
> - **Anaconda Prompt**: Shows `(base) C:\>` → use `set` command  
> - **Anaconda PowerShell Prompt**: Shows `(base) PS C:\>` → use `$env:` syntax

#### **Top 3 Common Mistakes**

1. **Wrapping the key in quotes inside the env-var dialog** → authentication fails  
2. **Leaving a space before/after the key** → authentication fails  
3. **Using wrong syntax for your shell type:**
   - Using `set` in PowerShell → variable isn't exported  
   - Using `$env:` in CMD → command not recognized

#### **Command Syntax Reference**

| Task | CMD (Anaconda Prompt) | PowerShell (Anaconda PowerShell Prompt) |
|------|----------------------|------------------------------------------|
| **Set temp variable** | `set OPENAI_API_KEY=sk-xxx` | `$env:OPENAI_API_KEY="sk-xxx"` |
| **Check variable** | `echo %OPENAI_API_KEY%` | `$env:OPENAI_API_KEY` |
| **Set permanent** | `setx OPENAI_API_KEY "sk-xxx"` | `setx OPENAI_API_KEY "sk-xxx"` |
---

### 6. Run the app
#### 6-1. Type the following command in Anaconda Prompt to start the server:
```bash
python main.py
```
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

conda install -c conda-forge ffmpeg -y (if need)

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

### Analysis process
The analysis process of this project was conducted as follows:

- Model Performance Evaluation
  - We tested the accuracy of Whisper’s speech-to-text conversion using multiple audio recordings in different languages (Mandarin Chinese, English, and Korean). The         transcriptions were manually compared against the original text to assess recognition correctness.
  - Special attention was paid during testing to analyze whether the model could accurately recognize drink names.
- Translation and Correction Assessment
  - The raw text produced by Whisper was passed to GPT-4o for correction and subsequently translated into Traditional Chinese. We evaluated the translation accuracy with a focus on domain-specific expressions, such as drink names and flavor adjustments.
- Retrieval Results Analysis (RAG)
  - For the queries translated into Traditional Chinese, we examined whether the retrieved content from the menu database correctly corresponded to user inquiries.
  - We further analyzed the impact of different query phrasing on retrieval quality.
- Integrated Testing
  - We conducted end-to-end simulations of multi-turn conversations to observe the overall user experience from voice input to voice output.
  - Tests were performed under various conditions, including different languages, question lengths, and background noise scenarios.
  
### Insights
Based on the above analysis, we derived the following key findings:

- Whisper demonstrates robust multilingual support and achieves high recognition accuracy in quiet environments; however, performance degrades with background noise.
- Recognition of domain-specific terms, such as drink names, still shows some inaccuracies and requires contextual correction.
- Combining translation with retrieval-augmented generation (RAG) improves the relevance and precision of the model’s responses.
- Implementing voice interaction significantly lowers the technical barrier for consumers using this system and effectively reduces the workload of store staff during the ordering process.

## Results

![Model Output](Group_4_Talk-To-Cashier/notebooks/order.jpg)
picture 1

![Model Output](Group_4_Talk-To-Cashier/notebooks/order1.jpg)
picture 2

### Example Ordering Process
- First: asking for information of recent events

  The AI cashier will give the customers detail information of recent events of the shop.
  
- Second: ordering beverages
  
  The AI cashier will analysis the customers' oral orders, search for the target on the menu, ask for the sweet level and ice, and automatically calculate the price of the item. The customers can also change their orders to other beverages on the menu (demonstrated in the bottom of picture 1), or adding new items into the order (demonstrated in picture 2), the AI cashier will go through the same process again. If the customers want to end the ordering process, they just need to ask: "What's the total?" And the AI cashier will calculate the total amount of price and stop receive orders. Finally, the AI cashier will ask the customers if they bring reusable cups with them for a 5NTD discount.

![Model Output](Group_4_Talk-To-Cashier/notebooks/orderF.jpg)
picture 3

### Multilingual Support
- The AI cashier can support different foreign languages. Picture 3 shows example of ordering drinks in French, and the previous two pictures are Chinese examples.

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

## Contributors

| Responsibility                                  | Member Name         |
|-------------------------------------------------|---------------------|
| Programmer                                      | Kevin, Rick         |
| README Writing - Project Description            | Leo, Chloe          |
| README Writing - How to Install and Run         | Kevin, Rick         |
| README Writing - File Structure                 | Kevin, Rick         |
| README Writing - Analysis                       | Chloe               |
| README Writing - Results                        | Leo                 |
| README Writing - Include Credits                | Chloe               |
| README Writing - Contributions                  | Chloe               |
| README Writing - Add a License                  | Chloe, Robert       |
| README Writing - References                     | Robert              |
| Data Pre-processing                             | Leo, Chloe, Robert  |


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
