//microcontroller_h.h 
#include <stdint.h> 
#include "variables.h"
/**
 * @brief Enables the clock for GPIOA on the STM32F407 board.
 * 
 * This function directly manipulates the RCC AHB1 peripheral clock enable register
 * to enable the clock for GPIOA. It ensures that the GPIOA peripheral is powered
 * and ready for use.
 * 
 * @param None
 * @return None
 */
void ENABLE_GPIOA_CLOCK(void) {
    // Define the base address for the RCC AHB1 peripheral clock enable register
    volatile uint32_t *RCC_AHB1ENR = (uint32_t *)(0x40023800 + 0x30);

    // Enable the clock for GPIOA by setting the appropriate bit in the RCC AHB1ENR register
    *RCC_AHB1ENR |= (1 << 0);
}
