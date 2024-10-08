//microcontroller_h.h 
#include <stdint.h> 
#include "variables.h"

/**
 * @brief Configures the mode of a specified GPIO pin.
 * 
 * This function sets the mode of a GPIO pin to either input or output.
 * 
 * @param port_base The base address of the GPIO port.
 * @param pin The pin number to configure.
 * @param mode The mode to set for the pin (e.g., GPIO_MODE_INPUT, GPIO_MODE_OUTPUT_PP).
 * @retval None
 */
void set_input_output_mode(uint32_t port_base, uint16_t pin, uint32_t mode) {
    // Calculate the pin position
    uint32_t pin_position = 0;
    for (uint16_t temp_pin = pin; temp_pin > 1; temp_pin >>= 1) {
        pin_position++;
    }

    // Calculate the register address for the mode configuration
    volatile uint32_t *moder = (volatile uint32_t *)(port_base + 0x00); // GPIOx_MODER register offset is 0x00

    // Clear the existing mode bits for the pin
    *moder &= ~(0x3 << (pin_position * 2));

    // Set the new mode bits for the pin
    *moder |= (mode << (pin_position * 2));
}



/**
 * @brief  Enables the clock for GPIOA port.
 * @param  None
 * @retval None
 */
void ENABLE_GPIOA_CLOCK(void) {
    // Define the base address for RCC (Reset and Clock Control)
    const uint32_t RCC_BASE = 0x40023800;
    
    // Define the offset for AHB1ENR (AHB1 peripheral clock enable register)
    const uint32_t RCC_AHB1ENR_OFFSET = 0x30;
    
    // Define the bit position for GPIOA clock enable in the AHB1ENR register
    const uint32_t GPIOA_CLOCK_ENABLE_BIT = 0;
    
    // Calculate the address of the AHB1ENR register
    volatile uint32_t* RCC_AHB1ENR = (uint32_t*)(RCC_BASE + RCC_AHB1ENR_OFFSET);
    
    // Enable the clock for GPIOA by setting the corresponding bit in the AHB1ENR register
    *RCC_AHB1ENR |= (1 << GPIOA_CLOCK_ENABLE_BIT);
}



/**
 * @brief  Enables the clock for GPIO port B.
 * @param  None
 * @retval None
 */
void ENABLE_GPIOB_CLOCK(void) {
    // Define the base address for the RCC (Reset and Clock Control) registers
    const uint32_t RCC_BASE = 0x40023800;
    
    // Define the offset for the AHB1ENR (AHB1 peripheral clock enable register)
    const uint32_t RCC_AHB1ENR_OFFSET = 0x30;
    
    // Define the bit position for GPIOB clock enable in the AHB1ENR register
    const uint32_t GPIOB_CLOCK_ENABLE_BIT = 1;
    
    // Calculate the address of the AHB1ENR register
    volatile uint32_t* RCC_AHB1ENR = (uint32_t*)(RCC_BASE + RCC_AHB1ENR_OFFSET);
    
    // Enable the clock for GPIOB by setting the corresponding bit in the AHB1ENR register
    *RCC_AHB1ENR |= (1 << GPIOB_CLOCK_ENABLE_BIT);
}



/**
 * @brief  Enables the clock for GPIO port C.
 * @param  None
 * @retval None
 */
void ENABLE_GPIOC_CLOCK(void) {
    // Define the base address for the RCC (Reset and Clock Control) registers
    const uint32_t RCC_BASE = 0x40023800;
    
    // Define the offset for the AHB1ENR (AHB1 peripheral clock enable register)
    const uint32_t RCC_AHB1ENR_OFFSET = 0x30;
    
    // Define the bit position for GPIOC clock enable in the AHB1ENR register
    const uint32_t GPIOC_CLOCK_ENABLE_BIT = 2;
    
    // Calculate the address of the AHB1ENR register
    volatile uint32_t* RCC_AHB1ENR = (uint32_t*)(RCC_BASE + RCC_AHB1ENR_OFFSET);
    
    // Enable the clock for GPIOC by setting the corresponding bit in the AHB1ENR register
    *RCC_AHB1ENR |= (1 << GPIOC_CLOCK_ENABLE_BIT);
}



/**
 * @brief  Reads the state of a specific GPIO pin.
 * @param  port_base: Base address of the GPIO port.
 * @param  pin: Pin number to read.
 * @retval State of the pin (0 or 1).
 */
int hardware_abstraction_layer_function_gpio_read_pin(uint32_t port_base, uint16_t pin) {
    // Calculate the bit position of the pin
    uint32_t pin_position = 0;
    while ((pin >> pin_position) != 1) {
        pin_position++;
    }
    
    // Read the input data register (IDR) of the GPIO port
    uint32_t idr = *((volatile uint32_t *)(port_base + 0x10));
    
    // Extract the state of the specified pin
    return (idr & (1 << pin_position)) ? 1 : 0;
}



/**
 * @brief  Writes a value to a specific GPIO pin.
 * @param  port_base: Base address of the GPIO port.
 * @param  pin: Pin number to write to.
 * @param  value: Value to write to the pin (0 or 1).
 * @retval None
 */
void hardware_abstraction_layer_function_gpio_write_pin(uint32_t port_base, uint16_t pin, uint8_t value) {
    // Calculate the bit position of the pin
    uint32_t pin_position = 0;
    for (uint16_t temp_pin = pin; temp_pin > 1; temp_pin >>= 1) {
        pin_position++;
    }
    
    // Create a mask for the pin
    uint32_t pin_mask = 1 << pin_position;
    
    // Get the address of the Output Data Register (ODR)
    volatile uint32_t *odr = (volatile uint32_t *)(port_base + 0x14);
    
    // Write the value to the pin using bitwise operations
    if (value) {
        // Set the pin
        *odr |= pin_mask;
    } else {
        // Clear the pin
        *odr &= ~pin_mask;
    }
}



/**
 * @brief Toggles the state of a specified GPIO pin.
 * 
 * This function toggles the state of a GPIO pin on the STM32F407 board.
 * 
 * @param port_base The base address of the GPIO port.
 * @param pin The pin number to toggle.
 * @retval None
 */
void hardware_abstraction_layer_function_gpio_toggle_pin(uint32_t port_base, uint16_t pin) {
    // Calculate the bit position of the pin
    uint32_t pin_position = 0;
    for (uint16_t temp_pin = pin; temp_pin > 1; temp_pin >>= 1) {
        pin_position++;
    }
    
    // Create a mask for the pin
    uint32_t pin_mask = 1 << pin_position;
    
    // Get the address of the Output Data Register (ODR)
    volatile uint32_t *odr = (volatile uint32_t *)(port_base + 0x14);
    
    // Toggle the pin using bitwise operations
    *odr ^= pin_mask;
}



/**
 * @brief Delays execution for a specified amount of time.
 * 
 * This function creates a delay by executing nested loops. The delay time is
 * specified in arbitrary units and can be adjusted by changing the inner loop count.
 * 
 * @param delay_time The amount of delay time in arbitrary units.
 * @retval None
 */
void hardware_abstraction_layer_function_delay(uint32_t delay_time) {
    // Outer loop to create a larger delay
    for (uint32_t i = 0; i < delay_time; i++) {
        // Inner loop to create a smaller delay
        for (uint32_t j = 0; j < 1000; j++) {
            // No operation, just to waste time
            __asm__("nop");
        }
    }
}

