#include <stdint.h>
// Define the base address for USART2 peripheral on the STM32F407 board.
// This address is used to access the USART2 registers for configuration and data transmission.
// The base address is specific to the STM32F407 microcontroller.
#define USART2_BASE ((uint32_t)0x40004400)

// Define the USART_FLAG_TXE variable for the STM32F407 board
// This flag is used to indicate that the transmit data register is empty
// and ready for new data to be written. It is a part of the USART status register.
// The value is hardcoded based on the STM32F407 reference manual.
#define USART_FLAG_TXE ((uint16_t)0x0080)

// USART_CR1_OFFSET is the offset for the Control Register 1 of the USART peripheral.
// This offset is used to access the USART_CR1 register from the base address of a USART peripheral.
// The value is specific to the STM32F407 microcontroller series.
#define USART_CR1_OFFSET ((uint32_t)0x000C)

// Define the offset for the Data Register (DR) of the USART peripheral.
// This offset is used to access the data register of a USART peripheral
// on the STM32F407 microcontroller. The value is based on the reference
// manual for the STM32F407, which specifies the offset for the DR register
// within the USART peripheral's register map.
#define USART_DR_OFFSET ((uint32_t)0x04)

// Base address for the Reset and Clock Control (RCC) peripheral
#define RCC_BASE ((uint32_t)0x40023800)

// USART_SR_OFFSET is the offset for the Status Register of the USART peripheral.
// This offset is used to access the status register from the base address of a USART peripheral.
// The value is based on the STM32F407 reference manual.
#define USART_SR_OFFSET ((uint32_t)0x00)

// Define the offset for the AHB1 peripheral clock enable register in the RCC
// This offset is used to access the RCC_AHB1ENR register, which controls the clock
// for the AHB1 peripherals on the STM32F407 board.
#define RCC_AHB1ENR_OFFSET ((uint32_t)0x30)

// Define the offset for the Baud Rate Register (BRR) in the USART peripheral.
// This offset is used to calculate the address of the BRR register for a specific USART instance.
// The value is based on the STM32F407 reference manual, which specifies the register map for USART peripherals.
#define USART_BRR_OFFSET ((uint32_t)0x00000008)
