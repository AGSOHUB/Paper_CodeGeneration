from langchain_openai import OpenAIEmbeddings
import hashlib
import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

api_key = os.getenv("OPENAI_API_KEY")

vectorstore_path = "vector_stores"

def process_c_files(folder_path):
    """
    Processes specific C and header files within a folder to create or update 
    vector stores using embeddings. This function checks for file changes based 
    on content hashes and only processes files that are new or modified.

    Parameters:
    - folder_path (str): Path to the folder containing C and header files to process.

    Returns:
    - None: Updates vector stores and hash files locally.
    """
    # Initialize embeddings
    embeddings = OpenAIEmbeddings()

    # List of specific files to process
    specific_files = ['main.c', 'microcontroller_hal.h', 'variables.h', 'typedefs.h']

    # Always initialize a new vector store
    vectorstore = None

    # Walk through all files in the given folder and its subfolders
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename in specific_files:
                file_path = os.path.join(root, filename)
                print(f"Processing file: {filename}")

                # Compute hash of the file's content to detect changes
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                file_hash = hashlib.md5(file_content.encode('utf-8')).hexdigest()

                # Determine path for storing the hash specific to this file
                hash_filename = f"{filename}_hash.txt"
                hash_path = os.path.join(vectorstore_path, hash_filename)

                # Use TextLoader to load documents (assumes one document per file)
                loader = TextLoader(file_path)
                documents = loader.load()

                # Split the file content into chunks
                text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30, separator="\n")
                docs = text_splitter.split_documents(documents)

                # Create or update the vector store for the new/modified file
                if vectorstore is None:
                    vectorstore = FAISS.from_documents(docs, embeddings)
                else:
                    vectorstore.add_documents(docs)

                vectorstore.save_local(vectorstore_path)

                # Save the new hash for this file
                with open(hash_path, 'w') as f:
                    f.write(file_hash)

                print("Vector store for file updated and saved.")

    if vectorstore is not None:
        print("All files processed and vector stores updated.")
    else:
        print("No C or H files found in the directory.")

def generate_c_variable(variable_name):
    """
    Generates a C variable definition for a missing variable in a project targeting an STM32F407 board.
    """
    prompt_template = """
    Given the provided information about the existing code for an STM32F407 board:

    Please generate a C variable definition for the variable named '{variable_name}'. Use this exact name: '{variable_name}'.
    Only return the code for the variable definition, not any code that is already present. Use appropriate types and initializations for the STM32F407-Board. Don't reference new values that are not yet implemented. Only the ones already present. Hardcode the values. Never reference a new variable.

    return-format:
    - define statement for C-code variable
    - don't reference Typedefs like Gpio_pinstate or GPIO def. Keep in mind ports and pins defined like this:
      #define GPIO_PIN_11 ((uint16_t)0x0800)
      #define GPIOA ((uint32_t)0x40020000)
    - no further code. no pointers. no typedefs-references
    - the variable should be well-documented with comments explaining its purpose and initialization.
    """

    prompt = prompt_template.format(variable_name=variable_name)

    # Perform the similarity search in the vector store
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever()

    # Search the vector store for similar documents
    similar_docs = retriever.get_relevant_documents(variable_name)

    # Combine similar document content
    context = "\n".join([doc.page_content for doc in similar_docs])

    # Generate the initial prompt for the LLM
    prompt = prompt_template.format(variable_name=variable_name, context=context)

    # Use the generated prompt and context to create the function
    function_code = openai_prompt(prompt)

    #print("Generated function code:")
    #print(function_code)

    return function_code


def generate_c_function(function_name, parameters):
    """
    Generates a C function implementation for a missing function in a project targeting an STM32F407 board.
    """
    length_parameters = len(parameters.split(","))
    prompt_template = """

    You will be my Custom Hardware Abstraction Layer Generator. 

    Please generate a custom C function implementation for the function' {function_name}' with {length_parameters} parameters like: {parameters}. 
    These parameters are example parameters used. create the necessary input-parameters for the function.

    Only return the code for the custom hal-function implementation, not any code that is already present. Use constants for the STM32F407-Board.  
    
    Important:
    Ensure to calculate the GPIO pin position using a loop to properly determine the bit position for the pin configuration.
    Prefer to use direct manipulation of the output data register (ODR) using bitwise operations for toggling GPIO pins to ensure atomic and reliable operations.

    Donts:
    - dont return anything else than executable c-code
    Dont reference new variables or functions that are not implemented.
    Dont reference stm32fxxx_hal.h functions.
    Define statements are illegal in functions. if it should be a global variable, only reference it. dont implement it.
    Dont reference Typedefs like Gpio_pinstate or gpio def. keep in mind ports and pins defined like this(const uint16_t GPIO_PIN_11 = 0x0800); const uint32_t GPIOA = 0x40020000;)

    Return-format:
    - only return one c-code function {function_name} with comments to explain it. no include statements or variable initalizations
    - be well-documented with comments explaining its purpose, parameters, and return value
    - create own custom HAL-functions without referencing other functions
    - use the ports-base address. there are no Typedef.

    Create the {function_name} the provided information about the existing code for an STM32F407 board:

    {context}
    """
 
    
    
    print(f"\nLet's create some code\n\nFunction name: {function_name}\nParameters: {parameters}\n")


    # Perform the similarity search in the vector store
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever()
    
    # Search the vector store for similar documents
    similar_docs = retriever.get_relevant_documents(function_name)

    # Combine similar document content
    context = "\n".join([doc.page_content for doc in similar_docs])

    # Generate the initial prompt for the LLM
    prompt = prompt_template.format(function_name=function_name, context=context, parameters = parameters, length_parameters = length_parameters)

    # Use the generated prompt and context to create the functionS
    function_code = openai_prompt(prompt)
    #print(prompt)
    #print("Generated function code:")
    #print(function_code)

    return function_code


def generate_c_typedef(typedef_name):
    """
    Generates a C typedef definition for a missing typedef in a project targeting an STM32F407 board.
    """
    prompt_template = """
    Given the provided information about the existing code for an STM32F407 board:
    
    Please generate a C typedef definition for the type named '{typedef_name}'. Use this exact name: '{typedef_name}'
    Only return the code for the typedef definition, not any code that is already present. Use appropriate types and structures for the STM32F407-Board. Do not reference new values that are not yet implemented. Only the ones already present.

    The typedef should be well-documented with comments explaining its purpose.
    """

    prompt = prompt_template.format(typedef_name=typedef_name)

    # Perform the similarity search in the vector store
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever()
    
    # Search the vector store for similar documents
    similar_docs = retriever.get_relevant_documents(typedef_name)

    # Combine similar document content
    context = "\n".join([doc.page_content for doc in similar_docs])

    # Generate the initial prompt for the LLM
    prompt = prompt_template.format(typedef_name=typedef_name, context=context)

    # Use the generated prompt and context to create the typedef
    typedef_code = openai_prompt(prompt)

    #print("Generated typedef code:")
    #print(typedef_code)

    return typedef_code



def openai_prompt(prompt_text):
    """
    Sends a prompt to the OpenAI GPT model and retrieves the generated response.

    Parameters:
    - prompt_text (str): The text prompt to be sent to the OpenAI model.

    Returns:
    - str: The content of the response generated by the OpenAI model.
    """
        
    # Instantiate the OpenAI model object
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    # Define the messages for the OpenAI call
    messages = [
        ("system", "You are a helpful assistant that responds to user prompts."),
        ("human", prompt_text),
    ]

    # Invoke the OpenAI model with the messages
    ai_msg = llm.invoke(messages)

    # Return the content of the response
    return ai_msg.content