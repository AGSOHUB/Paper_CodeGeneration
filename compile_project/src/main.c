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

// Simple function to convert an integer to a string (base 10)
void int_to_string(int num, char *str) {
    int i = 0;
    int is_negative = 0;

    // Handle negative numbers
    if (num < 0) {
        is_negative = 1;
        num = -num;
    }

    // Process each digit
    do {
        str[i++] = (num % 10) + '0';
        num /= 10;
    } while (num > 0);

    // If the number is negative, add the negative sign
    if (is_negative) {
        str[i++] = '-';
    }

    // Null-terminate the string
    str[i] = '\0';

    // Reverse the string
    int start = 0;
    int end = i - 1;
    while (start < end) {
        char temp = str[start];
        str[start] = str[end];
        str[end] = temp;
        start++;
        end--;
    }
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
    int successful_functions = 0;  // Bitmask to track successful tests

    // Enable the clock for GPIOA
    ENABLE_GPIOA_CLOCK();

    // Check if GPIOA clock is enabled after calling ENABLE_GPIOA_CLOCK
    if (is_gpioa_clock_enabled()) {
        // print("Log: GPIOA clock is enabled.\n");
        successful_functions |= 1 << 0;  // First test passed, set bit 0
    } else {
        // print("Log: Failed to enable GPIOA clock!\n");
        successful_functions |= 0 << 0;  // First test failes, set bit 0 to 0
    }

    // Configure GPIOA Pin 5 as output after enabling the clock
    set_input_output_mode(0x40020000, 1 << 5, 1);  // GPIOA_BASE = 0x40020000

    // Write to GPIOA Pin 5 after enabling the clock
    hardware_abstraction_layer_function_gpio_write_pin(0x40020000, 1 << 5, 1);

    // Check if the pin is set to high
    if (hardware_abstraction_layer_function_gpio_read_pin(0x40020000, 1 << 5)) {
        // print("Test: Pin is correctly set to HIGH after enabling clock!\n");
        successful_functions |= 1 << 1;  // Second test passed, set bit 1
    } else {
        // print("Test: Pin is NOT set to HIGH after enabling clock.\n");
        successful_functions |= 0 << 1;  // Second test failes, set to 0
    }

    // Toggle the pin to low
    hardware_abstraction_layer_function_gpio_toggle_pin(0x40020000, 1 << 5);

    // Check if the pin is toggled to low
    if (!hardware_abstraction_layer_function_gpio_read_pin(0x40020000, 1 << 5)) {
        // print("Test: Pin toggled to LOW successfully!\n");
        successful_functions |= 1 << 2;  // Third test passed, set bit 2
    } else {
        // print("Test: Pin toggle failed, still HIGH.\n");
        successful_functions |= 0 << 2;  // Third test failes, set bit 2 to 0
    }

    // Convert the integer to a string
    char number_str[12];  // Buffer for the integer-to-string conversion
    int_to_string(successful_functions, number_str);  // Convert the integer to string

    // Print the resulting string
    print(number_str);


    // Loop forever
    while (1);

    return 0;
}