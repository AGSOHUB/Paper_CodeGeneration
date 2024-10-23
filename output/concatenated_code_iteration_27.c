#include <stdint.h>

//typedefs.h 


// Define the offset for the USART_CR1 register in the STM32F407 microcontroller.
// This offset is used to access the control register 1 of the USART peripheral.
// The value is hardcoded based on the STM32F407 reference manual.
#define USART_CR1_OFFSET ((uint32_t)0x000C)

// USART_FLAG_TXE is a flag used to indicate that the USART transmit data register is empty.
// This flag is typically used in USART status register (USART_SR) to check if the USART is ready to send more data.
// The value 0x0080 corresponds to the bit position of the TXE flag in the USART status register.
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
// The value is derived from the STM32F407 reference manual, which specifies the offset for the USART_SR register.
#define USART_SR_OFFSET ((uint32_t)0x00)

// Define the offset for the Baud Rate Register (BRR) in the USART peripheral.
// This offset is used to calculate the address of the BRR register for a given USART instance.
// The value is based on the STM32F407 reference manual, which specifies the register map for USART peripherals.
#define USART_BRR_OFFSET ((uint32_t)0x08)

// Define the base address for USART2 peripheral on the STM32F407 board.
// This address is used to access the USART2 registers for configuration and data transmission.
// The base address is specific to the STM32F407 microcontroller.
#define USART2_BASE ((uint32_t)0x40004400)

// USART_DR_OFFSET is the offset for the Data Register in the USART peripheral.
// This offset is used to access the data register for reading or writing data.
// The value is specific to the STM32F407 microcontroller series.
#define USART_DR_OFFSET ((uint32_t)0x04)

//microcontroller_h.h 
 


// Function to set the mode of a GPIO pin as input or output
// Parameters:
// - gpio_base: Base address of the GPIO port (e.g., 0x40020000 for GPIOA)
// - pin_mask: Bitmask representing the pin (e.g., 1 << 5 for pin 5)
// - mode: 0 for input, 1 for output
/**
 * @brief Writes a value to a specific GPIO pin.
 * 
 * This function sets or resets a specific GPIO pin by directly manipulating
 * the Output Data Register (ODR) of the specified GPIO port. It ensures atomic
 * operations using bitwise operations.
 *
 * @param gpio_port_base The base address of the GPIO port (e.g., 0x40020000 for GPIOA).
 * @param pin_mask A mask indicating the specific pin to write to (e.g., 1 << 5 for pin 5).
 * @param value The value to write to the pin (1 to set the pin, 0 to reset the pin).
 */
void hardware_abstraction_layer_function_gpio_write_pin(uint32_t gpio_port_base, uint32_t pin_mask, uint32_t value) {
    // Calculate the address of the Output Data Register (ODR) for the given GPIO port
    volatile uint32_t *GPIO_ODR = (uint32_t *)(gpio_port_base + 0x14);
    // Determine the pin position by finding the first set bit in the pin_mask
    uint32_t pin_position = 0;
    uint32_t temp_mask = pin_mask;
    while (temp_mask >>= 1) {
        pin_position++;
    }
    // Use bitwise operations to set or reset the pin
    if (value) {
        // Set the pin: Use bitwise OR to set the specific bit in the ODR
        *GPIO_ODR |= (1 << pin_position);
    } else {
        // Reset the pin: Use bitwise AND with NOT to clear the specific bit in the ODR
        *GPIO_ODR &= ~(1 << pin_position);
    }
}
/**
 * @brief Toggles the state of a specific GPIO pin.
 * 
 * This function toggles the state of a GPIO pin specified by the port base address and pin mask.
 * It calculates the pin position and uses bitwise XOR to toggle the specific bit in the Output Data Register (ODR).
 * 
 * @param gpio_port_base The base address of the GPIO port (e.g., 0x40020000 for GPIOA).
 * @param pin_mask The mask of the pin to toggle (e.g., 1 << 5 for pin 5).
 */
void hardware_abstraction_layer_function_gpio_toggle_pin(uint32_t gpio_port_base, uint32_t pin_mask) {
    // Calculate the address of the Output Data Register (ODR) for the given GPIO port
    volatile uint32_t *GPIO_ODR = (uint32_t *)(gpio_port_base + 0x14);
    // Determine the pin position by finding the first set bit in the pin_mask
    uint32_t pin_position = 0;
    uint32_t temp_mask = pin_mask;
    while (temp_mask >>= 1) {
        pin_position++;
    }
    // Toggle the pin: Use bitwise XOR to toggle the specific bit in the ODR
    *GPIO_ODR ^= (1 << pin_position);
}
/**
 * @brief Enables the clock for GPIOA on the STM32F407 board.
 * 
 * This function sets the appropriate bit in the RCC AHB1 peripheral clock enable register
 * to enable the clock for GPIOA. This is necessary before any GPIOA operations can be performed.
 * 
 * @return void
 */
void ENABLE_GPIOA_CLOCK(void) {
    // Define the base address for the RCC AHB1 peripheral clock enable register
    volatile uint32_t *RCC_AHB1ENR = (uint32_t *)(0x40023800 + 0x30); // RCC_BASE + RCC_AHB1ENR_OFFSET
    // Set the bit 0 to enable the clock for GPIOA
    *RCC_AHB1ENR |= (1 << 0);
}
/**
 * @brief Configures a GPIO pin as input or output on the STM32F407 board.
 * 
 * This function sets the mode of a specific GPIO pin to either input or output.
 * It calculates the pin position from the pin mask and directly manipulates
 * the GPIO mode register to set the desired mode.
 * 
 * @param gpio_base Base address of the GPIO port (e.g., 0x40020000 for GPIOA)
 * @param pin_mask Bitmask representing the pin (e.g., 1 << 5 for pin 5)
 * @param mode 0 for input, 1 for output
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
    // Clear the two bits corresponding to the pin number
    *GPIO_MODER &= ~(0x3 << (pin_number * 2));
    // Set the mode for the pin (0 for input, 1 for output)
    *GPIO_MODER |= (mode << (pin_number * 2));
}

/**
 * @brief Reads the state of a specific GPIO pin on the STM32F407 board.
 * 
 * This function reads the input data register (IDR) of a specified GPIO port
 * to determine the state of a specific pin.
 * 
 * @param port_base_address The base address of the GPIO port (e.g., 0x40020000 for GPIOA).
 * @param pin_mask The mask of the pin to read (e.g., 1 << 5 for pin 5).
 * @return 1 if the pin is high, 0 if the pin is low.
 */
int hardware_abstraction_layer_function_gpio_read_pin(uint32_t port_base_address, uint32_t pin_mask) {
    // Calculate the address of the Input Data Register (IDR) for the given GPIO port
    volatile uint32_t *GPIO_IDR = (uint32_t *)(port_base_address + 0x10);
    
    // Determine the pin position by finding the first set bit in the pin_mask
    uint32_t pin_position = 0;
    uint32_t temp_mask = pin_mask;
    while (temp_mask >>= 1) {
        pin_position++;
    }
    
    // Read the pin state: Check if the specific bit in the IDR is set
    return ((*GPIO_IDR & (1 << pin_position)) != 0) ? 1 : 0;
}

