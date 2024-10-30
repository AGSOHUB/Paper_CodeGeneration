//microcontroller_h.h 
#include <stdint.h> 
#include "variables.h"
#include <stdint.h>
// Function to set the mode of a GPIO pin as input or output
// Parameters:
// - gpio_base: Base address of the GPIO port (e.g., 0x40020000 for GPIOA)
// - pin_mask: Bitmask representing the pin (e.g., 1 << 5 for pin 5)
// - mode: 0 for input, 1 for output
/**
 * @brief Toggles a specific GPIO pin on the STM32F407 board.
 *
 * This function directly manipulates the Output Data Register (ODR) of a specified GPIO port
 * to toggle the state of a specific pin. It uses bitwise XOR operations, which is crucial
 * in embedded systems to avoid race conditions.
 *
 * @param gpio_port_base The base address of the GPIO port (e.g., 0x40020000 for GPIOA).
 * @param pin_mask A bitmask representing the pin to toggle (e.g., 1 << 5 for pin 5).
 */
void hardware_abstraction_layer_function_gpio_toggle_pin(uint32_t gpio_port_base, uint32_t pin_mask) {
    // Calculate the address of the Output Data Register (ODR)
    volatile uint32_t *ODR = (uint32_t *)(gpio_port_base + 0x14);
    // Determine the bit position of the pin
    uint32_t pin_position = 0;
    while ((pin_mask >> pin_position) != 1) {
        pin_position++;
    }
    // Toggle the pin: use bitwise XOR to toggle the specific bit
    *ODR ^= (1 << pin_position);
}
/**
 * @brief Writes a value to a specific GPIO pin on the STM32F407 board.
 *
 * This function directly manipulates the Output Data Register (ODR) of a specified GPIO port
 * to set or clear a specific pin. It calculates the pin position using a loop to ensure
 * the correct bit is modified.
 *
 * @param gpio_port_base The base address of the GPIO port (e.g., 0x40020000 for GPIOA).
 * @param pin_mask A bitmask representing the pin to write to (e.g., 1 << 5 for pin 5).
 * @param value The value to write to the pin (0 to clear, any non-zero value to set).
 * @return None
 */
void hardware_abstraction_layer_function_gpio_write_pin(uint32_t gpio_port_base, uint32_t pin_mask, uint32_t value) {
    // Calculate the address of the Output Data Register (ODR)
    volatile uint32_t *ODR = (uint32_t *)(gpio_port_base + 0x14);
    // Determine the bit position of the pin
    uint32_t pin_position = 0;
    while ((pin_mask >> pin_position) != 1) {
        pin_position++;
    }
    // Write the value to the pin using bitwise operations
    if (value) {
        // Set the pin high
        *ODR |= (1 << pin_position);
    } else {
        // Set the pin low
        *ODR &= ~(1 << pin_position);
    }
}
/**
 * @brief Enables the clock for GPIOA on the STM32F407 board.
 *
 * This function sets the appropriate bit in the RCC AHB1 peripheral clock enable register
 * to enable the clock for GPIOA. This is necessary before any GPIOA operations can be performed.
 *
 * @return None
 */
void ENABLE_GPIOA_CLOCK(void) {
    // Define the base address for the RCC AHB1 peripheral clock enable register
    volatile uint32_t *RCC_AHB1ENR = (uint32_t *)(0x40023800 + 0x30); // RCC base address + AHB1ENR offset
    // Set the bit 0 to enable the clock for GPIOA
    *RCC_AHB1ENR |= (1 << 0);
}
/**
 * @brief Reads the state of a specific GPIO pin on the STM32F407 board.
 *
 * This function directly accesses the Input Data Register (IDR) of a specified GPIO port
 * to read the state of a specific pin. It calculates the pin position using a loop to ensure
 * the correct bit is checked.
 *
 * @param gpio_port_base The base address of the GPIO port (e.g., 0x40020000 for GPIOA).
 * @param pin_mask A bitmask representing the pin to read (e.g., 1 << 5 for pin 5).
 * @return int Returns 1 if the pin is high, 0 if the pin is low.
 */
int hardware_abstraction_layer_function_gpio_read_pin(uint32_t gpio_port_base, uint32_t pin_mask) {
    // Calculate the address of the Input Data Register (IDR)
    volatile uint32_t *IDR = (uint32_t *)(gpio_port_base + 0x10);
    // Determine the bit position of the pin
    uint32_t pin_position = 0;
    while ((pin_mask >> pin_position) != 1) {
        pin_position++;
    }
    // Read the pin state: use bitwise AND to check the specific bit
    return ((*IDR & (1 << pin_position)) != 0) ? 1 : 0;
}
