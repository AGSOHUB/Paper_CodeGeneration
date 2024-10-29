#include <stdint.h>

//typedefs.h 


// Base address for the Reset and Clock Control (RCC) peripheral
// on the STM32F407 microcontroller. This address is used to access
// the RCC registers for configuring the clock system of the MCU.
#define RCC_BASE ((uint32_t)0x40023800)

// Define the offset for the Baud Rate Register (BRR) in the USART peripheral.
// This offset is used to calculate the address of the BRR register for a given USART instance.
// The value is based on the STM32F407 reference manual, which specifies the register map for USART peripherals.
#define USART_BRR_OFFSET ((uint32_t)0x00000008)

// USART_SR_OFFSET is the offset for the Status Register of the USART peripheral.
// This offset is used to access the status register from the base address of a USART peripheral.
// The value is derived from the STM32F407 reference manual.
#define USART_SR_OFFSET ((uint32_t)0x00)

// USART_DR_OFFSET is the offset for the Data Register in the USART peripheral.
// This offset is used to access the data register for reading or writing data.
// The value is specific to the STM32F407 microcontroller series.
#define USART_DR_OFFSET ((uint32_t)0x04)

// Define the base address for USART2 peripheral on the STM32F407 board.
// This address is used to access the USART2 registers for configuration and data transmission.
#define USART2_BASE ((uint32_t)0x40004400)

// Define the offset for the AHB1 peripheral clock enable register in the RCC
// This offset is used to access the RCC_AHB1ENR register, which controls the clock
// for the AHB1 peripherals on the STM32F407 board.
#define RCC_AHB1ENR_OFFSET ((uint32_t)0x30)

// Define the offset for the USART_CR1 register in the STM32F407 microcontroller.
// This offset is used to access the control register 1 of the USART peripheral.
// The value is hardcoded based on the STM32F407 reference manual.
#define USART_CR1_OFFSET ((uint32_t)0x000C)

// USART_FLAG_TXE is a flag used to indicate that the USART transmit data register is empty.
// This flag is typically used in USART status register to check if the USART is ready to send more data.
// The value is hardcoded based on the STM32F407 reference manual.
#define USART_FLAG_TXE ((uint16_t)0x0080)

//microcontroller_h.h 
 


// Function to set the mode of a GPIO pin as input or output
// Parameters:
// - gpio_base: Base address of the GPIO port (e.g., 0x40020000 for GPIOA)
// - pin_mask: Bitmask representing the pin (e.g., 1 << 5 for pin 5)
// - mode: 0 for input, 1 for output
// Function to set the mode of a GPIO pin as input or output
// Parameters:
// - gpio_base: Base address of the GPIO port (e.g., 0x40020000 for GPIOA)
// - pin_mask: Bitmask representing the pin (e.g., 1 << 5 for pin 5)
// - mode: 0 for input, 1 for output
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
void hardware_abstraction_layer_function_gpio_write_pin(uint32_t gpio_port_base, uint32_t pin_mask, uint32_t value) {
    // Calculate the address of the Output Data Register (ODR) for the given GPIO port
    volatile uint32_t *GPIO_ODR = (uint32_t *)(gpio_port_base + 0x14);
    // Determine the pin position by finding the first set bit in the pin_mask
    uint8_t pin_position = 0;
    while ((pin_mask >> pin_position) != 1) {
        pin_position++;
    }
    // Use bitwise operations to set or reset the pin
    if (value) {
        // Set the pin: Use bitwise OR to set the specific bit
        *GPIO_ODR |= (1 << pin_position);
    } else {
        // Reset the pin: Use bitwise AND with NOT to clear the specific bit
        *GPIO_ODR &= ~(1 << pin_position);
    }
}
void hardware_abstraction_layer_function_gpio_toggle_pin(uint32_t gpio_port_base, uint32_t pin_mask) {
    // Calculate the address of the Output Data Register (ODR) for the given GPIO port
    volatile uint32_t *GPIO_ODR = (uint32_t *)(gpio_port_base + 0x14);
    // Determine the pin position by finding the first set bit in the pin_mask
    uint8_t pin_position = 0;
    while ((pin_mask >> pin_position) != 1) {
        pin_position++;
    }
    // Toggle the pin: Use bitwise XOR to toggle the specific bit
    *GPIO_ODR ^= (1 << pin_position);
}
/**
 * @brief Sets the mode of a GPIO pin as input or output on the STM32F407 board.
 * 
 * This function configures a specific GPIO pin to operate either as an input or an output.
 * It directly manipulates the GPIO port's mode register (MODER) to set the desired mode.
 * 
 * @param gpio_base: Base address of the GPIO port (e.g., 0x40020000 for GPIOA)
 * @param pin_mask: Bitmask representing the pin (e.g., 1 << 5 for pin 5)
 * @param mode: 0 for input, 1 for output
 * @return None
 */
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
    // Set the mode for the pin
    if (mode == 1) {
        // Set as output
        *GPIO_MODER |= (0x1 << (pin_number * 2));
    } else {
        // Set as input (mode == 0)
        // No need to set bits as they are already cleared
    }
}

int hardware_abstraction_layer_function_gpio_read_pin(uint32_t gpio_port_base, uint32_t pin_mask) {
    // Calculate the address of the Input Data Register (IDR) for the given GPIO port
    volatile uint32_t *GPIO_IDR = (uint32_t *)(gpio_port_base + 0x10);

    // Determine the pin position by finding the first set bit in the pin_mask
    uint8_t pin_position = 0;
    while ((pin_mask >> pin_position) != 1) {
        pin_position++;
    }

    // Read the pin state: Use bitwise AND to check the specific bit in the IDR
    // Return 1 if the pin is high, 0 if the pin is low
    return ((*GPIO_IDR & (1 << pin_position)) != 0) ? 1 : 0;
}

