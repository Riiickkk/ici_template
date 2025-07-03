# Project Title

Talk-To-Cashier

## Project Description

The project Talk-to-Cashier aims to develop an AI-powered virtual cashier system designed to assist customers in ordering beverages at drink shops. The motivation behind this project stems from four common issues observed in traditional human-operated ordering and cashier processes: excessive workload on cashiers during peak hours, potential hygiene concerns when staff are required to handle both cashiering and drink preparation simultaneously, a high rate of human error, and a heavy dependence on manual labor in existing ordering systems.

By integrating speech recognition, natural language processing, and Retrieval-Augmented Generation (RAG) technologies, we built an AI cashier system capable of natural conversational interaction. The objective is to enable the AI cashier to receive and process verbal orders through speech recognition, accurately calculate the total amount based on selected items, and facilitate the checkout process via integrated payment functionalities. This approach aims to reduce labor demands, improve operational efficiency, and ensure a smooth and consistent customer experience.

For model training and testing, we selected the beverage brand “De Zheng” (得正) as our data source. The primary reason for choosing this brand lies in its relatively streamlined menu, which facilitates efficient and precise model training within the constraints of our limited resources and technical capacity, while also allowing us to focus on optimizing semantic understanding and menu structuring.

During development, we encountered several challenges, including training and deploying the RAG model in real-time interactive settings, building a structured menu database, and addressing information loss due to errors in speech recognition. We also placed particular emphasis on interface optimization and designed a voice-based interaction interface to enhance the system’s user-friendliness.

Looking forward, in response to an increasingly globalized society, we aim to expand the system’s multilingual support, incorporate more diverse ordering scenarios (e.g., dine-in vs. takeout options), further enhance the AI's semantic understanding and recommendation capabilities, and explore the feasibility of integration with more chain stores.

## How to Install and Run the Project

> The following instructions target **Windows 10/11 + Miniconda** because that is where most user mistakes occur.  
> macOS / Linux users can follow the **same steps**—just replace the installer, paths, and shell syntax that differ on your platform.

> ### 0. Prerequisites

| Item                | Get it here                                                     | Notes                                                             |
|---------------------|-----------------------------------------------------------------|-------------------------------------------------------------------|
| Miniconda (≈ 60 MB) | <https://docs.anaconda.com/free/miniconda/index.html>           | Install in a **pure-English path** such as `C:\Miniconda3`.       |
| Git                 | <https://git-scm.com/downloads>                                | For `git clone` (you can also download ZIP manually).             |
| OpenAI API Key      | <https://platform.openai.com/account/api-keys>                 | Make sure the key is **active** and your account still has credits.|

> **Why pure-English paths?**  
> Non-ASCII folders like `桌面` or OneDrive sync paths frequently cause path-encoding or permission errors on Windows.

## File Structure

[Describe the file structure of your project, including how the files are organized and what each file contains. Be sure to explain the purpose of each file and how they are related to one another.]

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
