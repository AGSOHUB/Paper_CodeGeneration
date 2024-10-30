#include <stdint.h>

//typedefs.h 


// USART_SR_OFFSET is the offset for the Status Register of the USART peripheral.
// This offset is used to access the status register from the base address of a USART peripheral.
// The value is specific to the STM32F407 microcontroller series.
#define USART_SR_OFFSET ((uint32_t)0x00)

// Define the base address for USART2 peripheral on the STM32F407 board.
// This address is used to access the USART2 registers for configuration and data transmission.
// The base address is specific to the STM32F407 microcontroller.
#define USART2_BASE ((uint32_t)0x40004400)

// USART_FLAG_TXE is a flag used to indicate that the USART transmit data register is empty.
// This flag is typically used in USART status register (USART_SR) to check if the USART is ready to send more data.
#define USART_FLAG_TXE ((uint16_t)0x0080)

// Define the offset for the Data Register (DR) of the USART peripheral.
// This offset is used to access the data register of a USART peripheral
// on the STM32F407 microcontroller. The value is based on the reference
// manual for the STM32F407, which specifies the offset for the DR register
// within the USART peripheral's register map.
#define USART_DR_OFFSET ((uint32_t)0x04)

// Define the offset for the AHB1 peripheral clock enable register in the RCC
// This offset is used to access the RCC_AHB1ENR register, which controls the clock
// for the AHB1 peripherals on the STM32F407 microcontroller.
#define RCC_AHB1ENR_OFFSET ((uint32_t)0x30)

// Base address for the Reset and Clock Control (RCC) peripheral
// on the STM32F407 microcontroller. This address is used to access
// the RCC registers for configuring the clock system of the MCU.
#define RCC_BASE ((uint32_t)0x40023800)

// USART_BRR_OFFSET is the offset for the Baud Rate Register in the USART peripheral.
// This offset is used to calculate the address of the Baud Rate Register for a specific USART instance.
// The value is based on the STM32F407 reference manual, which specifies the register map for USART peripherals.
#define USART_BRR_OFFSET ((uint32_t)0x00000008)

// USART_CR1_OFFSET is the offset for the Control Register 1 of the USART peripheral.
// This offset is used to access the USART_CR1 register from the base address of a USART peripheral.
// The value is specific to the STM32F407 microcontroller series.
#define USART_CR1_OFFSET ((uint32_t)0x000C)

//microcontroller_h.h 
 


// Function to set the mode of a GPIO pin as input or output
// Parameters:
// - gpio_base: Base address of the GPIO port (e.g., 0x40020000 for GPIOA)
// - pin_mask: Bitmask representing the pin (e.g., 1 << 5 for pin 5)
// - mode: 0 for input, 1 for output
/**
 * @brief Reads the state of a specific GPIO pin.
 * 
 * This function reads the state of a GPIO pin specified by the port base address and pin mask.
 * It calculates the pin position and checks the input data register (IDR) to determine if the pin is high or low.
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
 * @brief Configures a GPIO pin as input or output.
 * 
 * This function sets the mode of a specific GPIO pin on the STM32F407 board.
 * It calculates the pin number from the provided pin mask and configures the
 * GPIO mode register (MODER) to set the pin as input or output.
 * 
 * @param gpio_base The base address of the GPIO port (e.g., 0x40020000 for GPIOA).
 * @param pin_mask A bitmask representing the pin (e.g., 1 << 5 for pin 5).
 * @param mode The mode to set for the pin: 0 for input, 1 for output.
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
    // If mode is 1, set the pin as output (01 in MODER)
    // If mode is 0, set the pin as input (00 in MODER)
    *GPIO_MODER |= (mode << (pin_number * 2));
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
 * @brief Toggles the state of a specific GPIO pin.
 * 
 * This function toggles the state of a GPIO pin specified by the port base address and pin mask.
 * It calculates the pin position and directly manipulates the output data register (ODR) to toggle the pin state.
 * 
 * @param gpio_port_base The base address of the GPIO port (e.g., 0x40020000 for GPIOA).
 * @param pin_mask The mask of the pin to toggle (e.g., 1 << 5 for pin 5).
 */
void hardware_abstraction_layer_function_gpio_toggle_pin(uint32_t gpio_port_base, uint32_t pin_mask) {
    // Calculate the address of the Output Data Register (ODR)
    volatile uint32_t *ODR = (uint32_t *)(gpio_port_base + 0x14);
    
    // Determine the bit position of the pin
    uint32_t pin_position = 0;
    while ((pin_mask >> pin_position) != 1) {
        pin_position++;
    }
    
    // Toggle the pin state using bitwise XOR operation
    *ODR ^= (1 << pin_position);
}

