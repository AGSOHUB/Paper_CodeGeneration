#include "microcontroller_hal.h"


void usart2_init() {
    volatile uint32_t *USART2_CR1 = (uint32_t *)(USART2_BASE + USART_CR1_OFFSET);
    volatile uint32_t *USART2_BRR = (uint32_t *)(USART2_BASE + USART_BRR_OFFSET);

    // Set the baud rate (assuming 16MHz clock, 9600 baud rate)
    *USART2_BRR = 0x683; // Example value for 9600 baud

    // Enable USART, Transmitter, and Receiver
    *USART2_CR1 |= (1 << 13) |  // UE: USART Enable
                   (1 << 3);    // TE: Transmitter Enable
}


// Function to send data over USART2
void print(char *data) {
    volatile uint32_t *USART2_SR = (uint32_t *)(USART2_BASE + USART_SR_OFFSET);
    volatile uint32_t *USART2_DR = (uint32_t *)(USART2_BASE + USART_DR_OFFSET);

    while (*data) {
        while (!(*USART2_SR & USART_FLAG_TXE)); // Wait until TX is ready
        *USART2_DR = (uint8_t)(*data++);
    }
    while (!(*USART2_SR & USART_FLAG_TXE)); // Wait until TX is ready
    *USART2_DR = '\n';
}



/**
 * @brief Checks if the clock for GPIOA is enabled.
 * 
 * @return 1 if the clock is enabled, 0 if not.
 */
int is_gpioa_clock_enabled(void) {
    volatile uint32_t *RCC_AHB1ENR = (uint32_t *)(RCC_BASE + RCC_AHB1ENR_OFFSET);
    return ((*RCC_AHB1ENR & (1 << 0)) != 0) ? 1 : 0;
}

int main() {
    usart2_init();

    // Enable the clock for GPIOA
    ENABLE_GPIOA_CLOCK();

    // Check if GPIOA clock is enabled after calling ENABLE_GPIOA_CLOCK
    if (is_gpioa_clock_enabled()) {
        print("Log: GPIOA clock is enabled.");
    } else {
        print("Log: Failed to enable GPIOA clock!");
    }

    // Configure GPIOA Pin 5 as output after enabling the clock
    set_input_output_mode(GPIOA_BASE, 1 << 5, 1);

    // Write to GPIOA Pin 5 after enabling the clock
    hardware_abstraction_layer_function_gpio_write_pin(GPIOA_BASE, 1 << 5, 1);

    // Check if the pin is set to high
    if (hardware_abstraction_layer_function_gpio_read_pin(GPIOA_BASE, 1 << 5)) {
        print("Test: Pin is correctly set to HIGH after enabling clock!");
    } else {
        print("Test: Pin is NOT set to HIGH after enabling clock.");
    }

    // Toggle the pin to low
    hardware_abstraction_layer_function_gpio_toggle_pin(GPIOA_BASE, 1 << 5);

    // Check if the pin is toggled to low
    if (!hardware_abstraction_layer_function_gpio_read_pin(GPIOA_BASE, 1 << 5)) {
        print("Test: Pin toggled to LOW successfully!");
    } else {
        print("Test: Pin toggle failed, still HIGH.");
    }

    // Loop forever
    while (1);

    return 0;
}
