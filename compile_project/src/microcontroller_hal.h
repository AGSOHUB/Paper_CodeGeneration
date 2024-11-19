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

#include <stdint.h>
// Function to set the mode of a GPIO pin as input or output
// Parameters:
// - gpio_base: Base address of the GPIO port (e.g., 0x40020000 for GPIOA)
// - pin_mask: Bitmask representing the pin (e.g., 1 << 5 for pin 5)
// - mode: 0 for input, 1 for output
void set_input_output_mode(uint32_t gpio_base, uint32_t pin_mask, uint8_t mode) {
    // Calculate the pin number from the pin mask
    uint8_t pin_number = 0;
    while ((pin_mask >> pin_number) != 1) {
        pin_number++;
    }

    // Calculate the address of the GPIO mode register (MODER)
    volatile uint32_t *GPIO_MODER = (uint32_t *)(gpio_base + 0x00);

    // Clear the two bits corresponding to the pin in the MODER register
    *GPIO_MODER &= ~(0x3 << (pin_number * 2));

    // Set the mode for the pin (0x1 for output, 0x0 for input)
    *GPIO_MODER |= (mode << (pin_number * 2));
}
