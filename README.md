<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Automated HAL Code Generation for Embedded Systems</title>
</head>
<body>
    <h1>Automated HAL Code Generation for Embedded Systems</h1>

    <h2>Abstract</h2>
    <p>
        This project presents a method to generate integrated software components for embedded systems,
        designed to seamlessly fit into existing implementations without requiring developer intervention.
        The approach is demonstrated by automatically generating hardware abstraction layer (HAL) code for
        GPIO operations on the STM32F407 microcontroller. By leveraging Abstract Syntax Trees (AST) to
        analyze existing code and Retrieval-Augmented Generation (RAG) to produce missing components, this
        method effectively enables code completion for embedded applications.
    </p>

    <h2>Setup Instructions</h2>

    <h3>Step 1: Download and Set Up MSYS2</h3>
    <ol>
        <li>
            Download the <a href="https://www.msys2.org/">MSYS2 installer</a> and install it on your system.
        </li>
        <li>
            Add the following directories to your system PATH:
            <ul>
                <li><code>C:\msys64\mingw64\bin</code></li>
                <li><code>C:\msys64\usr\bin</code></li>
            </ul>
        </li>
    </ol>

    <h3>Step 2: Install Required Packages</h3>
    <p>Open the MSYS2 terminal and run the following commands to install necessary packages:</p>
    <pre><code>pacman -S mingw-w64-x86_64-arm-none-eabi-gcc
pacman -S make
pacman -S mingw-w64-x86_64-cmake</code></pre>

    <h3>Step 3: Install Python Dependencies</h3>
    <p>Ensure you have Python installed, then run the following command to install the required Python packages:</p>
    <pre><code>pip install -r requirements.txt</code></pre>

    <h3>Step 4: Install Renode</h3>
    <ol>
        <li>
            Download the <a href="https://renode.io/download">Renode .MSI installer</a> and install Renode on your system.
        </li>
        <li>
            Add the Renode installation directory to your system PATH.
        </li>
    </ol>

    <h3>Step 5: Configure OpenAI Key</h3>
    <p>Add your OpenAI API key to a <code>.env</code> file in the project root directory:</p>
    <pre><code>OPENAI_API_KEY=your_openai_key</code></pre>

    <h2>Usage</h2>
    <p>
        With the environment set up, you can now use the project to generate HAL code for embedded systems by following
        the instructions in the main script.
    </p>
</body>
</html>
