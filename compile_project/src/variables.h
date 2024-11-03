#include <stdint.h>
// Define the offset for the Data Register (DR) of the USART peripheral.
// This offset is used to access the data register of a USART peripheral
// on the STM32F407 microcontroller. The value is based on the reference manual.
#define USART_DR_OFFSET ((uint32_t)0x04)

// Define the base address for USART2 peripheral on the STM32F407 board.
// This address is used to access the USART2 registers for configuration and data transmission.
#define USART2_BASE ((uint32_t)0x40004400)

// USART_FLAG_TXE is a flag used to indicate that the transmit data register is empty.
// This flag is typically used in USART communication to check if the USART is ready to send more data.
// The value 0x00000080 is a standard value for the TXE (Transmit Data Register Empty) flag in STM32 microcontrollers.
#define USART_FLAG_TXE ((uint32_t)0x00000080)

// Define the offset for the USART_CR1 register in the STM32F407 microcontroller.
// This offset is used to access the control register 1 of the USART peripheral.
// The value is hardcoded based on the STM32F407 reference manual.
#define USART_CR1_OFFSET ((uint32_t)0x000C)

// Define the offset for the Baud Rate Register (BRR) in the USART peripheral.
// This offset is used to calculate the address of the BRR register for a given USART instance.
// The value is based on the STM32F407 reference manual, which specifies the register map for USART peripherals.
#define USART_BRR_OFFSET ((uint32_t)0x00000008)

// USART_SR_OFFSET is the offset for the Status Register of the USART peripheral.
// This offset is used to access the status register from the base address of a USART peripheral.
// The value is based on the STM32F407 reference manual.
#define USART_SR_OFFSET ((uint32_t)0x00)

// Base address for the Reset and Clock Control (RCC) peripheral
// on the STM32F407 microcontroller. This address is used to access
// the RCC registers for configuring the clock system of the MCU.
#define RCC_BASE ((uint32_t)0x40023800)

// Define the offset for the AHB1 peripheral clock enable register in the RCC
// This offset is used to access the RCC_AHB1ENR register, which controls the clock
// for the AHB1 peripherals on the STM32F407 board.
#define RCC_AHB1ENR_OFFSET ((uint32_t)0x30)
