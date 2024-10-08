#include <stdint.h>
// Define the offset for the AHB1 peripheral clock enable register in the RCC (Reset and Clock Control) block.
// This offset is used to access the RCC_AHB1ENR register, which controls the clock for AHB1 peripherals.
// The offset value is based on the STM32F407 reference manual.
#define RCC_AHB1ENR_OFFSET ((uint32_t)0x30)
