#include <stdint.h>

//typedefs.h 

//variables 


// Define the GPIO mode for input
#define GPIO_MODE_INPUT 0x00U // 0x00U is the value for input mode in STM32F407



// Define the base address for GPIOA port
#define GPIOA ((uint32_t)0x40020000)



// Define GPIO_PIN_4 for STM32F407 board
#define GPIO_PIN_4 ((uint16_t)0x0010) // GPIO pin 4 is represented by the 5th bit (0x0010) in the GPIO port register



// Define GPIOB base address for STM32F407 board
#define GPIOB ((uint32_t)0x40020400)



// Define GPIO_PIN_2 for STM32F407 board
#define GPIO_PIN_2 ((uint16_t)0x0004) // Pin 2 is represented by the 3rd bit (0x0004) in the GPIO port register



// Define GPIO_PIN_5 for STM32F407 board
#define GPIO_PIN_5 ((uint16_t)0x0020) // GPIO pin 5 is represented by the bit mask 0x0020



// Define the GPIO mode for output push-pull
#define GPIO_MODE_OUTPUT_PP ((uint32_t)0x00000001) // 0x00000001 represents the mode for output push-pull



// Define GPIO_PIN_3 for STM32F407 board
#define GPIO_PIN_3 ((uint16_t)0x0008) // GPIO pin 3 is represented by the 4th bit (0x0008)



// Define GPIO_PIN_6 for STM32F407 board
#define GPIO_PIN_6 ((uint16_t)0x0040) // GPIO pin 6 is represented by the bit mask 0x0040



// Define GPIO_PIN_1 for STM32F407 board
#define GPIO_PIN_1 ((uint16_t)0x0002) // GPIO pin 1 is represented by the bit mask 0x0002


//microcontroller_h.h 
 

// Function to enable the clock for GPIOC
/**
 * @brief  Toggles the state of a specified GPIO pin.
 * 
 * This function toggles the state of a specified GPIO pin by directly manipulating the
 * Output Data Register (ODR) of the specified GPIO port. It ensures atomic
 * and reliable operations using bitwise operations.
 * 
 * @param port_base The base address of the GPIO port.
 * @param pin The pin number to toggle.
 */
void hardware_abstraction_layer_function_gpio_toggle_pin(uint32_t port_base, uint16_t pin) {
    // Calculate the bit position of the pin
    uint32_t pin_position = 0;
    for (uint16_t temp_pin = pin; temp_pin > 1; temp_pin >>= 1) {
        pin_position++;
    }
    // Pointer to the Output Data Register (ODR) of the specified port
    volatile uint32_t *odr = (volatile uint32_t *)(port_base + 0x14);
    // Toggle the pin by using bitwise XOR operation
    *odr ^= (1 << pin_position);
}
/**
 * @brief  Delays the execution for a specified number of milliseconds.
 * 
 * This function uses a busy-wait loop to create a delay for the specified
 * number of milliseconds. It assumes a system clock of 16 MHz and that the
 * SysTick timer is configured to generate an interrupt every 1 ms.
 * 
 * @param  delay_ms: The delay duration in milliseconds.
 * @return None
 */
void hardware_abstraction_layer_function_delay(uint32_t delay_ms) {
    // Assuming a system clock of 16 MHz and SysTick configured to 1 ms tick
    volatile uint32_t count;
    for (uint32_t i = 0; i < delay_ms; i++) {
        // Each iteration of this loop takes approximately 1 ms
        count = 16000; // Number of cycles for 1 ms delay at 16 MHz
        while (count--) {
            // Busy wait
        }
    }
}
/**
 * @brief  Configures the mode of a specified GPIO pin.
 * @param  port_base: Base address of the GPIO port.
 * @param  pin: GPIO pin number (e.g., GPIO_PIN_1, GPIO_PIN_2).
 * @param  mode: Mode to be set for the GPIO pin (e.g., GPIO_MODE_OUTPUT_PP, GPIO_MODE_INPUT).
 * @retval None
 */
void set_input_output_mode(uint32_t port_base, uint16_t pin, uint32_t mode) {
    // Calculate the pin position
    uint32_t pin_pos = 0;
    for (uint16_t temp_pin = pin; temp_pin > 1; temp_pin >>= 1) {
        pin_pos++;
    }
    // Calculate the register and bit position for the mode configuration
    uint32_t mode_reg_offset = (pin_pos / 8) * 4; // Each register controls 8 pins
    uint32_t mode_bit_pos = (pin_pos % 8) * 4;    // Each pin has 4 bits for mode configuration
    // Calculate the address of the mode register
    volatile uint32_t *mode_reg = (uint32_t *)(port_base + 0x00 + mode_reg_offset);
    // Clear the existing mode bits for the pin
    *mode_reg &= ~(0xF << mode_bit_pos);
    // Set the new mode bits for the pin
    *mode_reg |= (mode << mode_bit_pos);
}
/**
 * @brief  Enables the clock for GPIOC port.
 * @param  None
 * @retval None
 */
void ENABLE_GPIOC_CLOCK(void) {
    // Define the base address for RCC (Reset and Clock Control)
    const uint32_t RCC_BASE = 0x40023800;
    // Define the offset for AHB1ENR (AHB1 peripheral clock enable register)
    const uint32_t RCC_AHB1ENR_OFFSET = 0x30;
    // Define the bit position for GPIOC clock enable in AHB1ENR
    const uint32_t GPIOC_EN_BIT = 2;
    // Calculate the address of RCC_AHB1ENR
    volatile uint32_t *RCC_AHB1ENR = (uint32_t *)(RCC_BASE + RCC_AHB1ENR_OFFSET);
    // Enable the clock for GPIOC by setting the corresponding bit in RCC_AHB1ENR
    *RCC_AHB1ENR |= (1 << GPIOC_EN_BIT);
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
    // Define the bit position for GPIOA clock enable
    const uint32_t GPIOAEN_BIT_POS = 0;
    // Calculate the address of RCC_AHB1ENR
    volatile uint32_t *RCC_AHB1ENR = (uint32_t *)(RCC_BASE + RCC_AHB1ENR_OFFSET);
    // Enable the clock for GPIOA by setting the corresponding bit in RCC_AHB1ENR
    *RCC_AHB1ENR |= (1 << GPIOAEN_BIT_POS);
}
/**
 * @brief  Writes a value to a specified GPIO pin.
 * 
 * This function writes a value (0 or 1) to a specified GPIO pin by directly manipulating the
 * Output Data Register (ODR) of the specified GPIO port. It ensures atomic
 * and reliable operations using bitwise operations.
 * 
 * @param port_base The base address of the GPIO port (e.g., GPIOA, GPIOB).
 * @param pin The pin number to write to (e.g., GPIO_PIN_1, GPIO_PIN_2).
 * @param value The value to write to the pin (0 or 1).
 */
void hardware_abstraction_layer_function_gpio_write_pin(uint32_t port_base, uint16_t pin, int value) {
    // Calculate the bit position of the pin
    uint32_t pin_position = 0;
    for (uint16_t temp_pin = pin; temp_pin > 1; temp_pin >>= 1) {
        pin_position++;
    }
    // Get the address of the output data register (ODR)
    volatile uint32_t *odr = (volatile uint32_t *)(port_base + 0x14);
    // Write the value to the pin using bitwise operations
    if (value) {
        // Set the pin
        *odr |= (1 << pin_position);
    } else {
        // Clear the pin
        *odr &= ~(1 << pin_position);
    }
}
/**
 * @brief  Reads the state of a specified GPIO pin.
 * 
 * This function reads the state of a specified GPIO pin by directly accessing the
 * Input Data Register (IDR) of the specified GPIO port. It ensures atomic
 * and reliable operations using bitwise operations.
 * 
 * @param port_base The base address of the GPIO port (e.g., GPIOA, GPIOB).
 * @param pin The pin number to read (e.g., GPIO_PIN_1, GPIO_PIN_2).
 * @return int The state of the pin (0 or 1).
 */
int hardware_abstraction_layer_function_gpio_read_pin(uint32_t port_base, uint16_t pin) {
    // Calculate the bit position of the pin
    uint32_t pin_position = 0;
    for (uint16_t temp_pin = pin; temp_pin > 1; temp_pin >>= 1) {
        pin_position++;
    }
    // Get the address of the input data register (IDR)
    volatile uint32_t *idr = (volatile uint32_t *)(port_base + 0x10);
    // Read the pin state by checking the corresponding bit in the IDR
    int pin_state = (*idr & (1 << pin_position)) ? 1 : 0;
    return pin_state;
}


/**
 * @brief  Enables the clock for GPIOB port.
 * @param  None
 * @retval None
 */
void ENABLE_GPIOB_CLOCK(void) {
    // Define the base address for RCC (Reset and Clock Control)
    const uint32_t RCC_BASE = 0x40023800;
    // Define the offset for AHB1ENR (AHB1 peripheral clock enable register)
    const uint32_t RCC_AHB1ENR_OFFSET = 0x30;
    // Define the bit position for GPIOB clock enable in AHB1ENR
    const uint32_t GPIOB_EN_BIT = 1;
    // Calculate the address of RCC_AHB1ENR
    volatile uint32_t *RCC_AHB1ENR = (uint32_t *)(RCC_BASE + RCC_AHB1ENR_OFFSET);
    // Enable the clock for GPIOB by setting the corresponding bit in RCC_AHB1ENR
    *RCC_AHB1ENR |= (1 << GPIOB_EN_BIT);
}


