# Filename: test-renode.robot
*** Settings ***
Suite Setup                     Setup
Suite Teardown                  Teardown
Test Setup                      Reset Emulation
Resource                        ${RENODEKEYWORDS}
Library                         ReadUartViaPutty.py

*** Variables ***
${PLATFROM}                     ${CURDIR}\\renode-config_bvt.resc
${UART}                         sysbus.usart2
${HOST}                         localhost
${PORT}                         3456
${HOST_NAME}                    term
${UART_RESPONSE}                Hello World!

*** Keywords ***
Prepare the HW set up
    Execute Script              ${PLATFROM}
    Create Terminal Tester      ${UART}
Prepare UART Connection
    Execute Command             emulation CreateServerSocketTerminal ${PORT} "${HOST_NAME}" false
    Execute Command             connector Connect ${UART} ${HOST_NAME} 

*** Test Cases ***
UART Transmission Test - Renode
    [Timeout]    1m
    Prepare the HW set up
    Start Emulation
    Wait For Line On Uart       ${UART_RESPONSE}


UART Transmission Test - Socket
    [Timeout]    1m
    Prepare the HW set up
    Prepare UART Connection
    socket connect              ${HOST}    ${PORT}
    Start Emulation
    ${response}=                read from socket      # Adjust buffer size as needed
    socket disconnect
    Should Contain              ${response}    ${UART_RESPONSE}
    