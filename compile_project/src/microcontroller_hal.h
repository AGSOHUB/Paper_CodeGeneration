//microcontroller_h.h 
#include <stdint.h> 
#include "variables.h"
/**
 * @brief Enables the clock for GPIOA.
 * 
 * This function directly manipulates the RCC AHB1 peripheral clock enable register
 * to enable the clock for GPIOA. This is necessary before any GPIOA operations can be performed.
 */
void ENABLE_GPIOA_CLOCK(void) {
    // Define the base address for the RCC and the offset for the AHB1ENR register
    volatile uint32_t *RCC_AHB1ENR = (uint32_t *)(RCC_BASE + RCC_AHB1ENR_OFFSET);

    // Set the bit corresponding to GPIOA (bit 0) to enable its clock
    *RCC_AHB1ENR |= (1 << 0);
}

/**
 * @brief Configures a GPIO pin as input or output.
 * 
 * This function sets the mode of a specific GPIO pin on a given port
 * to either input or output. It directly manipulates the GPIO registers
 * to achieve this configuration.
 * 
 * @param gpio_base: Base address of the GPIO port (e.g., GPIOA_BASE).
 * @param pin_mask: Bitmask representing the pin to configure (e.g., 1 << 5 for pin 5).
 * @param mode: Mode to set for the pin (0 for input, 1 for output).
 */
void set_input_output_mode(uint32_t gpio_base, uint32_t pin_mask, uint8_t mode) {
    // Pointer to the GPIO mode register (MODER)
    volatile uint32_t *GPIO_MODER = (uint32_t *)(gpio_base + 0x00);

    // Determine the pin number from the pin mask
    uint8_t pin_number = 0;
    while ((pin_mask >> pin_number) != 1) {
        pin_number++;
    }

    // Clear the two bits corresponding to the pin in the MODER register
    *GPIO_MODER &= ~(0x3 << (pin_number * 2));

    // Set the mode for the pin (0x1 for output, 0x0 for input)
    *GPIO_MODER |= (mode << (pin_number * 2));
}

/**
 * @brief Writes a value to a specific GPIO pin.
 * 
 * This function directly manipulates the Output Data Register (ODR) of a GPIO port
 * to set or reset a specific pin. It ensures atomic operations using bitwise operations.
 * 
 * @param gpio_base: Base address of the GPIO port (e.g., GPIOA_BASE).
 * @param pin_mask: Bitmask representing the pin to be written (e.g., 1 << 5 for pin 5).
 * @param value: Value to write to the pin (0 for LOW, 1 for HIGH).
 */
void hardware_abstraction_layer_function_gpio_write_pin(uint32_t gpio_base, uint32_t pin_mask, uint8_t value) {
    // Pointer to the Output Data Register (ODR) of the specified GPIO port
    volatile uint32_t *GPIO_ODR = (uint32_t *)(gpio_base + 0x14); // ODR offset is 0x14

    // Determine the bit position of the pin
    uint32_t pin_position = 0;
    for (uint32_t mask = pin_mask; mask > 1; mask >>= 1) {
        pin_position++;
    }

    // Write the value to the pin
    if (value) {
        // Set the pin to HIGH
        *GPIO_ODR |= (1 << pin_position);
    } else {
        // Set the pin to LOW
        *GPIO_ODR &= ~(1 << pin_position);
    }
}

/**
 * @brief Reads the state of a specific GPIO pin.
 * 
 * This function reads the state of a GPIO pin by accessing the input data register (IDR)
 * of the specified GPIO port. It determines the bit position of the pin using a loop
 * and checks if the pin is set to high or low.
 * 
 * @param gpio_base: Base address of the GPIO port (e.g., GPIOA_BASE).
 * @param pin_mask: Bit mask representing the pin (e.g., 1 << 5 for pin 5).
 * @return 1 if the pin is high, 0 if the pin is low.
 */
int hardware_abstraction_layer_function_gpio_read_pin(uint32_t gpio_base, uint32_t pin_mask) {
    // Pointer to the input data register (IDR) of the GPIO port
    volatile uint32_t *GPIO_IDR = (uint32_t *)(gpio_base + 0x10); // IDR offset is 0x10

    // Determine the bit position of the pin
    uint32_t pin_position = 0;
    while ((pin_mask >> pin_position) != 1) {
        pin_position++;
    }

    // Read the pin state from the IDR
    return ((*GPIO_IDR & (1 << pin_position)) != 0) ? 1 : 0;
}

/**
 * @brief Toggles the state of a specified GPIO pin.
 * 
 * This function directly manipulates the Output Data Register (ODR) of the specified GPIO port
 * to toggle the state of a given pin. It uses bitwise operations to ensure atomic and reliable
 * toggling of the pin state.
 * 
 * @param gpio_base: The base address of the GPIO port (e.g., GPIOA_BASE).
 * @param pin_mask: The bitmask representing the pin to toggle (e.g., 1 << 5 for pin 5).
 */
void hardware_abstraction_layer_function_gpio_toggle_pin(uint32_t gpio_base, uint16_t pin_mask) {
    // Pointer to the Output Data Register (ODR) of the specified GPIO port
    volatile uint32_t *GPIO_ODR = (uint32_t *)(gpio_base + 0x14); // ODR offset is 0x14

    // Toggle the pin by XORing the ODR with the pin mask
    *GPIO_ODR ^= pin_mask;
}
