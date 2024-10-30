#include <stdint.h>

//typedefs.h 


// USART_DR_OFFSET is the offset for the Data Register in the USART peripheral.
// This offset is used to access the data register for reading or writing data.
// The value is specific to the STM32F407 microcontroller series.
#define USART_DR_OFFSET ((uint32_t)0x04)

// Define the base address for USART2 peripheral on the STM32F407 board.
// This address is used to access the USART2 registers for configuration and data transmission.
#define USART2_BASE ((uint32_t)0x40004400)

// Define the offset for the Baud Rate Register (BRR) in the USART peripheral.
// This offset is used to calculate the address of the BRR register for a given USART instance.
// The value is based on the STM32F407 reference manual, where the BRR register is located
// at an offset of 0x08 from the base address of the USART peripheral.
#define USART_BRR_OFFSET ((uint32_t)0x08)

// USART_FLAG_TXE is a flag used to indicate that the transmit data register is empty.
// This flag is typically used in USART communication to check if the USART is ready to send more data.
// The value 0x00000080 is a standard value for the TXE (Transmit Data Register Empty) flag in STM32 microcontrollers.
#define USART_FLAG_TXE ((uint16_t)0x0080)

// Define the offset for the AHB1 peripheral clock enable register in the RCC
// This offset is used to access the RCC_AHB1ENR register, which controls the clock
// for the AHB1 peripherals on the STM32F407 board.
#define RCC_AHB1ENR_OFFSET ((uint32_t)0x30)

// Base address for the Reset and Clock Control (RCC) peripheral
// on the STM32F407 microcontroller. This address is used to access
// the RCC registers for configuring the clock system of the MCU.
#define RCC_BASE ((uint32_t)0x40023800)

// USART_SR_OFFSET is the offset for the Status Register of the USART peripheral.
// This offset is used to access the status register from the base address of a USART peripheral.
// The value is specific to the STM32F407 microcontroller series.
#define USART_SR_OFFSET ((uint32_t)0x00)

// USART_CR1_OFFSET is the offset for the Control Register 1 of the USART peripheral.
// This offset is used to access the specific register within the USART peripheral's memory map.
// The value is hardcoded based on the STM32F407 reference manual.
#define USART_CR1_OFFSET ((uint32_t)0x000C)

//microcontroller_h.h 
 

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
    // Enable the clock for GPIOA by setting the 0th bit of the RCC_AHB1ENR register
    *RCC_AHB1ENR |= (1 << 0);
}

// Function to set the mode of a GPIO pin as input or output
// Parameters:
// - gpio_base: Base address of the GPIO port (e.g., 0x40020000 for GPIOA)
// - pin_mask: Bitmask representing the pin (e.g., 1 << 5 for pin 5)
// - mode: 0 for input, 1 for output
void set_input_output_mode(uint32_t gpio_base, uint32_t pin_mask, uint8_t mode) {
    // Calculate the pin position by finding the first set bit in pin_mask
    uint8_t pin_position = 0;
    for (uint32_t mask = pin_mask; mask > 1; mask >>= 1) {
        pin_position++;
    }
    // Calculate the address of the GPIO mode register (MODER)
    volatile uint32_t *GPIO_MODER = (uint32_t *)(gpio_base + 0x00);
    // Clear the two bits corresponding to the pin position
    *GPIO_MODER &= ~(0x3 << (pin_position * 2));
    // Set the mode: 0x1 for output, 0x0 for input
    *GPIO_MODER |= (mode & 0x1) << (pin_position * 2);
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
 * @brief Reads the state of a specified GPIO pin.
 * 
 * This function calculates the pin position and checks the input data register (IDR)
 * to determine if the pin is high or low.
 * 
 * @param port_base_address The base address of the GPIO port (e.g., 0x40020000 for GPIOA).
 * @param pin_mask The mask of the pin to read (e.g., 1 << 5 for pin 5).
 * @return 1 if the pin is high, 0 if the pin is low.
 */
int hardware_abstraction_layer_function_gpio_read_pin(uint32_t port_base_address, uint32_t pin_mask) {
    // Pointer to the input data register (IDR) of the GPIO port
    volatile uint32_t *GPIO_IDR = (uint32_t *)(port_base_address + 0x10);
    // Calculate the pin position by finding the first set bit in the pin mask
    uint32_t pin_position = 0;
    while ((pin_mask >> pin_position) != 1) {
        pin_position++;
    }
    // Read the pin state from the IDR and return 1 if high, 0 if low
    return ((*GPIO_IDR & (1 << pin_position)) != 0) ? 1 : 0;
}

/**
 * @brief Toggles the state of a specified GPIO pin.
 * 
 * This function directly manipulates the Output Data Register (ODR) of the GPIO port
 * to toggle the state of a specific pin. It ensures atomic operations using bitwise XOR.
 * 
 * @param gpio_port_base The base address of the GPIO port (e.g., 0x40020000 for GPIOA).
 * @param pin_mask The bitmask representing the pin to toggle (e.g., 1 << 5 for pin 5).
 */
void hardware_abstraction_layer_function_gpio_toggle_pin(uint32_t gpio_port_base, uint32_t pin_mask) {
    // Calculate the address of the Output Data Register (ODR) for the given GPIO port
    volatile uint32_t *ODR = (uint32_t *)(gpio_port_base + 0x14);
    // Toggle the specified pin using XOR operation
    *ODR ^= pin_mask;
}

