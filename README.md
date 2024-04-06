

# ChatBot Ecl

This is an academic project in ECL done by the students : Karouma Youssef, Khatib Mohamed and Tibi Daniel. The project aims to respond to questions relative to regulations in ECL.
## Table of Contents

- [Introduction](#ChatBot-Ecl)
- [Table of Contents](#table-of-contents)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Choice of Llama2 Quantisation](#choice-of-llama2-quantisation)
- [Usage](#usage)
- [Notes](#notes)
- [Slides](#slides)
- [Bibliographie](#bibliographie)
## Prerequisites

Before you can start using the Bot, make sure you have the following prerequisites installed on your system:

- Python 3.6 or higher


## Installation

1. Clone this repository to your local machine.


2. Create a Python virtual environment :


3. Install the required Python packages:

The installation differ from Mac to Pcs with CPU only to PCs with GPUs,

### For Metal (apple) : 

- install the app XCode from apple store (make sure you have the last update of the macos)


- install llamacpp that takes into consideration gpu for mac:
    
You can use this command : 
    ```
    CMAKE_ARGS="-DLLAMA_METAL_EMBED_LIBRARY=ON -DLLAMA_METAL=on" pip install -U llama-cpp-python --no-cache-dir
    ```

Then install the requirements

    ```
    pip install -r requirements.txt
    ```
    
You might have to reinstall sometimes some packages. To find which ones, you can execute the ChatBot.py file and see if all the packages are installed or not (or check by pip list)
    
 
    

### For CPU only :    
install the requirements

    ```
    pip install -r requirements.txt
    ```
    

    
### For GPU : 
check the link below : 
https://medium.com/@ryan.stewart113/a-simple-guide-to-enabling-cuda-gpu-support-for-llama-cpp-python-on-your-os-or-in-containers-8b5ec1f912a4#:~:text=The%20first%20step%20in%20enabling,and%20run%20CUDA%2Daccelerated%20applications.

- We couldn't make it work for GPU but we think someone can get somewhere with that :)


## Choice of Llama2 Quantisation

If you want to understand what is the process of quantisation, you can check the link below : 
https://www.tensorops.ai/post/what-are-quantized-llms

All the quantisations of the 7B parameters' llama2 are in the link below : 
https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/tree/main

For an M1 chip with 8gbs of ram, the 4 bit quantisation was working just fine. 
The problem with higher quantisations was with the Ram. So if you have more ram you can go for higher quantisations.

After downloading the quantisation you want, make sure you make the file in the same folder of the project and change the #llama_2_name
variable in the script ChatBot.py to the name of the version that you downloaded.




## Usage

### The file ingest.py : 
- You can ignore it if you want to use only the documents that were given in this git
- This file should be run just one time. The data we worked with in the project is provided. You can add more if you want. When your documents are ready, you can run the file ingest.py in order to get your VectorStore (check the slides or the report).


### The ChatBot

The bot can be used in 2 different methods:

1. By the provided GUI from chainlit : 
You have to go to the folder where the project is in in your terminal (or in visual code studio) and type the command 

    ```
    chainlit run model.py
    ```
For chainlit, it is a package that is built in order to make the implementation of a GUI easy for ChatBot. It is not exclusive to this project. If you are building a ChatBot too, you can check the documentation if you want to implement it for your own ChatBot : 
https://docs.chainlit.io/get-started/overview


2. You can use only the script ChatBot.py : 
To do so, you have to uncommand the last while loop in the code. And then by executing the code you'll be able to chat with the bot.

## Notes : 
- In Mac, in order to know if you are using Metal or only CPU, you can check the initialisation of the Llama2. If the initialisation doesnt show Metal Buffer Size and shows only CPU Buffer Size, then you are only working on CPU, and the installation of llama-cpp wasn't quite right. 

- You can visit the Langchain page to learn how to apply theoretical knowledge into practical code. It's a framework designed to simplify the creation of applications using large language models. They offer pre-defined functions for this purpose. Here's the link to the page : https://www.langchain.com

## Slides : 

- In the folder slides, you will find the support used to present the project to the jury at ECL. It is a simplified way to explain the process of the work of the ChatBot

## Bibliography : 

- The bibliography folder gives the articles that took this project to its end. There is the article about MiniLM, the embedding that we used in order to acheive the CPU-Only solution. There is another article about Llama2 and why would it be an Llm working in a project of ChatBot, and finally there are 2 articles about the process of indexation (check slides and report) and how is faiss used. 

