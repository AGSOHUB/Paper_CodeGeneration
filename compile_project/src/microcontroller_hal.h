//microcontroller_h.h 
#include <stdint.h> 
#include "variables.h"
#include <stdint.h>
// Function to set the mode of a GPIO pin as input or output
// Parameters:
// - gpio_base: Base address of the GPIO port (e.g., 0x40020000 for GPIOA)
// - pin_mask: Bitmask representing the pin (e.g., 1 << 5 for pin 5)
// - mode: 0 for input, 1 for output
void set_input_output_mode(uint32_t gpio_base, uint32_t pin_mask, uint8_t mode) {
    // Calculate the pin position by finding the first set bit in pin_mask
    uint8_t pin_position = 0;
    while ((pin_mask >> pin_position) != 1) {
        pin_position++;
    }
    // Calculate the address of the GPIO mode register (MODER)
    volatile uint32_t *GPIO_MODER = (uint32_t *)(gpio_base + 0x00);
    // Clear the two bits corresponding to the pin position
    *GPIO_MODER &= ~(0x3 << (pin_position * 2));
    // Set the mode for the pin
    if (mode == 1) {
        // Set as output
        *GPIO_MODER |= (0x1 << (pin_position * 2));
    } else {
        // Set as input (default is already cleared)
    }
}
/**
 * @brief Writes a value to a specific GPIO pin.
 * 
 * This function directly manipulates the Output Data Register (ODR) of a GPIO port
 * to set or reset a specific pin. It ensures atomic operations using bitwise operations.
 * 
 * @param gpio_port_base The base address of the GPIO port (e.g., 0x40020000 for GPIOA).
 * @param pin_mask The bitmask representing the pin to be written (e.g., 1 << 5 for pin 5).
 * @param value The value to write to the pin (0 for low, 1 for high).
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
 * @brief Reads the state of a specific GPIO pin.
 * 
 * This function reads the state of a GPIO pin by accessing the input data register (IDR)
 * of the specified GPIO port. It calculates the bit position of the pin using a loop
 * and returns the state of the pin.
 * 
 * @param gpio_port_base The base address of the GPIO port (e.g., 0x40020000 for GPIOA).
 * @param pin_mask The mask of the pin to read (e.g., 1 << 5 for pin 5).
 * @return 1 if the pin is high, 0 if the pin is low.
 */
int hardware_abstraction_layer_function_gpio_read_pin(uint32_t gpio_port_base, uint32_t pin_mask) {
    // Pointer to the input data register (IDR) of the GPIO port
    volatile uint32_t *GPIO_IDR = (uint32_t *)(gpio_port_base + 0x10);
    // Calculate the pin position by finding the first set bit in the pin_mask
    uint32_t pin_position = 0;
    while ((pin_mask >> pin_position) != 1) {
        pin_position++;
    }
    // Read the pin state from the IDR and return it
    return ((*GPIO_IDR & (1 << pin_position)) != 0) ? 1 : 0;
}
/**
 * @brief Toggles the state of a specified GPIO pin.
 * 
 * This function directly manipulates the Output Data Register (ODR) of a GPIO port
 * to toggle the state of a specific pin. It ensures atomic operations using bitwise
 * XOR to flip the pin state.
 * 
 * @param gpio_port_base The base address of the GPIO port (e.g., 0x40020000 for GPIOA).
 * @param pin_mask The bitmask representing the pin to toggle (e.g., 1 << 5 for pin 5).
 */
void hardware_abstraction_layer_function_gpio_toggle_pin(uint32_t gpio_port_base, uint32_t pin_mask) {
    // Calculate the address of the Output Data Register (ODR) for the given GPIO port
    volatile uint32_t *GPIO_ODR = (uint32_t *)(gpio_port_base + 0x14);
    // Toggle the pin by XORing the ODR with the pin mask
    *GPIO_ODR ^= pin_mask;
}

/**
 * @brief Enables the clock for GPIOA on the STM32F407 board.
 * 
 * This function directly manipulates the RCC AHB1 peripheral clock enable register
 * to enable the clock for GPIOA. It ensures that the GPIOA peripheral is powered
 * and ready for use.
 * 
 * @return 1 if the clock was successfully enabled, 0 otherwise.
 */
int ENABLE_GPIOA_CLOCK(void) {
    // Define the base address for the RCC and the offset for the AHB1ENR register
    volatile uint32_t *RCC_AHB1ENR = (uint32_t *)(0x40023800 + 0x30);
    
    // Enable the clock for GPIOA by setting the 0th bit in the RCC_AHB1ENR register
    *RCC_AHB1ENR |= (1 << 0);
    
    // Return 1 if the clock is enabled, 0 otherwise
    return ((*RCC_AHB1ENR & (1 << 0)) != 0) ? 1 : 0;
}
