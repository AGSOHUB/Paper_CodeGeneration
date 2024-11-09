# Automated HAL Code Generation for Embedded Systems

## Abstract
This project presents a method to generate integrated software components for embedded systems, designed to seamlessly fit into existing implementations without requiring developer intervention. The approach is demonstrated by automatically generating hardware abstraction layer (HAL) code for GPIO operations on the STM32F407 microcontroller. By leveraging Abstract Syntax Trees (AST) to analyze existing code and Retrieval-Augmented Generation (RAG) to produce missing components, this method effectively enables code completion for embedded applications.

## Setup Instructions

### Step 1: Download and Set Up MSYS2
1. Download the [MSYS2 installer](https://www.msys2.org/) and install it on your system.
2. Add the following directories to your system PATH:
   - `C:\msys64\mingw64\bin`
   - `C:\msys64\usr\bin`

### Step 2: Install Required Packages
Open the MSYS2 terminal and run the following commands to install necessary packages:

```bash
pacman -S mingw-w64-x86_64-arm-none-eabi-gcc
pacman -S make
pacman -S mingw-w64-x86_64-cmake
```

### Step 3: Install Python Dependencies
Ensure you have Python installed, then run the following command to install the required Python packages:

```bash
pip install -r requirements.txt
```

### Step 4: Install Renode
1. Download the [Renode .MSI installer](https://renode.io/download) and install Renode on your system.
2. Add the Renode installation directory to your system PATH.
   
### Step 5: Configure OpenAI Key
Add your OpenAI API key to a `.env` file in the project root directory:

```bash
OPENAI_API_KEY=your_openai_key
```
