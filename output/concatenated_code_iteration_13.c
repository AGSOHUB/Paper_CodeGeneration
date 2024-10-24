#include <stdint.h>

//typedefs.h 


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

//microcontroller_h.h 
 


// Function to set the mode of a GPIO pin as input or output
// Parameters:
// - port_base: Base address of the GPIO port (e.g., 0x40020000 for GPIOA)
// - pin_mask: Bitmask representing the pin (e.g., 1 << 5 for pin 5)
// - mode: 0 for input, 1 for output
// Function to set the mode of a GPIO pin as input or output
// Parameters:
// - port_base: Base address of the GPIO port (e.g., 0x40020000 for GPIOA)
// - pin_mask: Bitmask representing the pin (e.g., 1 << 5 for pin 5)
// - mode: 0 for input, 1 for output
void set_input_output_mode(uint32_t port_base, uint32_t pin_mask, uint8_t mode) {
    // Calculate the pin number from the pin mask
    uint8_t pin_number = 0;
    while ((pin_mask >> pin_number) != 1) {
        pin_number++;
    }
    // Calculate the address of the GPIO mode register (MODER)
    volatile uint32_t *GPIO_MODER = (uint32_t *)(port_base + 0x00);
    // Clear the two bits corresponding to the pin in the MODER register
    *GPIO_MODER &= ~(0x3 << (pin_number * 2));
    // Set the mode for the pin
    // 0x1 for output mode, 0x0 for input mode
    *GPIO_MODER |= (mode & 0x1) << (pin_number * 2);
}
/**
 * @brief Toggles the state of a specified GPIO pin.
 *
 * This function directly manipulates the Output Data Register (ODR) of a GPIO port
 * to toggle the state of a specific pin. It ensures atomic operations using bitwise XOR.
 * 
 * @param gpio_port_base The base address of the GPIO port (e.g., 0x40020000 for GPIOA).
 * @param pin_mask The bitmask representing the pin to toggle (e.g., 1 << 5 for pin 5).
 */
void hardware_abstraction_layer_function_gpio_toggle_pin(uint32_t gpio_port_base, uint32_t pin_mask) {
    // Calculate the address of the Output Data Register (ODR) for the given GPIO port
    volatile uint32_t *ODR = (uint32_t *)(gpio_port_base + 0x14);
    // Determine the bit position of the pin
    uint32_t pin_position = 0;
    while ((pin_mask >> pin_position) != 1) {
        pin_position++;
    }
    // Toggle the pin using XOR operation
    *ODR ^= (1 << pin_position);
}
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
/**
 * @brief Reads the state of a specific GPIO pin.
 * 
 * This function reads the state of a GPIO pin by accessing the input data register (IDR)
 * of the specified GPIO port. It calculates the bit position of the pin using a loop
 * to ensure accurate pin configuration.
 * 
 * @param gpio_port_base The base address of the GPIO port (e.g., 0x40020000 for GPIOA).
 * @param pin_mask The mask representing the pin to read (e.g., 1 << 5 for pin 5).
 * 
 * @return 1 if the pin is high, 0 if the pin is low.
 */
int hardware_abstraction_layer_function_gpio_read_pin(uint32_t gpio_port_base, uint32_t pin_mask) {
    // Pointer to the Input Data Register (IDR) of the GPIO port
    volatile uint32_t *IDR = (uint32_t *)(gpio_port_base + 0x10);
    // Determine the bit position of the pin
    uint32_t pin_position = 0;
    while ((pin_mask >> pin_position) != 1) {
        pin_position++;
    }
    // Read the state of the pin from the IDR
    return ((*IDR & (1 << pin_position)) != 0) ? 1 : 0;
}

/**
 * @brief Writes a specified value to a GPIO pin.
 *
 * This function directly manipulates the Output Data Register (ODR) of a GPIO port
 * to set or clear a specific pin. It ensures atomic operations using bitwise operations.
 *
 * @param gpio_port_base The base address of the GPIO port (e.g., 0x40020000 for GPIOA).
 * @param pin_mask The bit mask representing the pin to be written (e.g., 1 << 5 for pin 5).
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

