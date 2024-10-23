#include <stdint.h>

//typedefs.h 


// Define the offset for the USART_CR1 register in the STM32F407 microcontroller.
// This offset is used to access the control register 1 of the USART peripheral.
// The value is hardcoded based on the STM32F407 reference manual.
#define USART_CR1_OFFSET ((uint32_t)0x000C)

// Define the offset for the Data Register (DR) of the USART peripheral.
// This offset is used to access the data register of a USART peripheral
// on the STM32F407 microcontroller. The value is based on the reference
// manual for the STM32F407, which specifies the offset for the DR register
// within the USART peripheral's register map.
#define USART_DR_OFFSET ((uint32_t)0x04)

// Define the USART_FLAG_TXE variable for the STM32F407 board
// This flag is used to indicate that the transmit data register is empty
// and ready to accept new data for transmission. It is a part of the USART
// status register (USART_SR) and is typically used in USART communication
// to check if the transmitter is ready to send more data.
#define USART_FLAG_TXE ((uint16_t)0x0080)

// Define the base address for USART2 peripheral on the STM32F407 board.
// This address is used to access the USART2 registers for configuration and data transmission.
// The base address is specific to the STM32F407 microcontroller.
#define USART2_BASE ((uint32_t)0x40004400)

#define RCC_BASE ((uint32_t)0x40023800) // Base address for the Reset and Clock Control (RCC) registers on the STM32F407 board

// Define the offset for the Baud Rate Register (BRR) in the USART peripheral
// This offset is used to calculate the address of the BRR register for a given USART instance
// The value is based on the STM32F407 reference manual, where the BRR register is located
// at an offset of 0x08 from the base address of the USART peripheral.
#define USART_BRR_OFFSET ((uint32_t)0x08)

// USART_SR_OFFSET is the offset for the Status Register of the USART peripheral.
// This offset is used to access the status register from the base address of a USART peripheral.
// The value is derived from the STM32F407 reference manual.
#define USART_SR_OFFSET ((uint32_t)0x00)

// Define the offset for the AHB1 peripheral clock enable register in the RCC
// This offset is used to access the RCC_AHB1ENR register, which controls the clock
// for the AHB1 peripherals on the STM32F407 board.
#define RCC_AHB1ENR_OFFSET ((uint32_t)0x30)

//microcontroller_h.h 
 


// Function to set the mode of a GPIO pin as input or output
// Parameters:
// - port_base: Base address of the GPIO port (e.g., 0x40020000 for GPIOA)
// - pin_mask: Bitmask representing the pin (e.g., 1 << 5 for pin 5)
// - mode: 0 for input, 1 for output
/**
 * @brief Toggles the state of a specified GPIO pin.
 * 
 * This function directly manipulates the Output Data Register (ODR) of a GPIO port
 * to toggle the state of a specific pin. It uses bitwise operations to ensure atomic
 * and reliable toggling of the pin state.
 * 
 * @param gpio_port_base The base address of the GPIO port (e.g., 0x40020000 for GPIOA).
 * @param pin_mask The bitmask representing the pin to toggle (e.g., 1 << 5 for pin 5).
 */
void hardware_abstraction_layer_function_gpio_toggle_pin(uint32_t gpio_port_base, uint32_t pin_mask) {
    // Calculate the address of the Output Data Register (ODR) for the given GPIO port
    volatile uint32_t *ODR = (uint32_t *)(gpio_port_base + 0x14);
    // Toggle the pin by XORing the ODR with the pin mask
    *ODR ^= pin_mask;
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
    // Define the base address for the RCC and the offset for the AHB1ENR register
    volatile uint32_t *RCC_AHB1ENR = (uint32_t *)(0x40023800 + 0x30);
    // Set the bit corresponding to GPIOA (bit 0) to enable its clock
    *RCC_AHB1ENR |= (1 << 0);
}
// Function to set the mode of a GPIO pin as input or output
// Parameters:
// - port_base: Base address of the GPIO port (e.g., 0x40020000 for GPIOA)
// - pin_mask: Bitmask representing the pin (e.g., 1 << 5 for pin 5)
// - mode: 0 for input, 1 for output
void set_input_output_mode(uint32_t port_base, uint32_t pin_mask, uint8_t mode) {
    // Calculate the pin position by finding the first set bit in pin_mask
    uint8_t pin_position = 0;
    while ((pin_mask >> pin_position) != 1) {
        pin_position++;
    }
    // Calculate the address of the GPIO mode register (MODER)
    volatile uint32_t *GPIO_MODER = (uint32_t *)(port_base + 0x00);
    // Clear the two bits corresponding to the pin position
    *GPIO_MODER &= ~(0x3 << (pin_position * 2));
    // Set the mode: 0x1 for output, 0x0 for input
    *GPIO_MODER |= (mode << (pin_position * 2));
}
/**
 * @brief Writes a value to a specified GPIO pin.
 * 
 * This function directly manipulates the output data register (ODR) of the specified GPIO port
 * to set or reset the specified pin. It ensures atomic operations using bitwise operations.
 * 
 * @param gpio_port_base The base address of the GPIO port (e.g., 0x40020000 for GPIOA).
 * @param pin_mask The mask of the pin to write (e.g., 1 << 5 for pin 5).
 * @param value The value to write to the pin (1 for high, 0 for low).
 */
void hardware_abstraction_layer_function_gpio_write_pin(uint32_t gpio_port_base, uint32_t pin_mask, uint32_t value) {
    // Pointer to the output data register (ODR) of the GPIO port
    volatile uint32_t *GPIO_ODR = (uint32_t *)(gpio_port_base + 0x14);
    // Calculate the pin position by finding the first set bit in the pin_mask
    uint32_t pin_position = 0;
    while ((pin_mask >> pin_position) != 1) {
        pin_position++;
    }
    // Use bitwise operations to set or reset the pin
    if (value) {
        // Set the pin to high
        *GPIO_ODR |= (1 << pin_position);
    } else {
        // Set the pin to low
        *GPIO_ODR &= ~(1 << pin_position);
    }
}

/**
 * @brief Reads the state of a specified GPIO pin.
 * 
 * This function reads the input data register (IDR) of the specified GPIO port
 * to determine the state of the specified pin. It calculates the pin position
 * using a loop to find the first set bit in the pin mask.
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

