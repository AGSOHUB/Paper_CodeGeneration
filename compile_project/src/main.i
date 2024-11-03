# 0 "compile_project\\src\\main.c"
# 0 "<built-in>"
# 0 "<command-line>"
# 1 "compile_project\\src\\main.c"
# 1 "compile_project\\src\\microcontroller_hal.h" 1

# 1 "compile_project\\fake_libc_include/stdint.h" 1



typedef signed char int8_t;
typedef unsigned char uint8_t;
typedef short int16_t;
typedef unsigned short uint16_t;
typedef int int32_t;
typedef unsigned int uint32_t;
typedef long long int64_t;
typedef unsigned long long uint64_t;
# 3 "compile_project\\src\\microcontroller_hal.h" 2
# 1 "compile_project\\src\\variables.h" 1
# 4 "compile_project\\src\\microcontroller_hal.h" 2
# 2 "compile_project\\src\\main.c" 2


void usart2_init() {
    volatile uint32_t *USART2_CR1 = (uint32_t *)(USART2_BASE + USART_CR1_OFFSET);
    volatile uint32_t *USART2_BRR = (uint32_t *)(USART2_BASE + USART_BRR_OFFSET);


    *USART2_BRR = 1667;


    *USART2_CR1 |= (1 << 13) |
                   (1 << 3);
}



void print(char *data) {
    volatile uint32_t *USART2_SR = (uint32_t *)(USART2_BASE + USART_SR_OFFSET);
    volatile uint32_t *USART2_DR = (uint32_t *)(USART2_BASE + USART_DR_OFFSET);

    while (*data) {
        while (!(*USART2_SR & USART_FLAG_TXE));
        *USART2_DR = (uint8_t)(*data++);
    }
    while (!(*USART2_SR & USART_FLAG_TXE));
    *USART2_DR = '\n';
}


void int_to_string(int num, char *str) {
    int i = 0;
    int is_negative = 0;


    if (num < 0) {
        is_negative = 1;
        num = -num;
    }


    do {
        str[i++] = (num % 10) + '0';
        num /= 10;
    } while (num > 0);


    if (is_negative) {
        str[i++] = '-';
    }


    str[i] = '\0';


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






int is_gpioa_clock_enabled(void) {
    volatile uint32_t *RCC_AHB1ENR = (uint32_t *)(RCC_BASE + RCC_AHB1ENR_OFFSET);
    return ((*RCC_AHB1ENR & (1 << 0)) != 0) ? 1 : 0;
}

int main() {
    usart2_init();
    int successful_functions = 0;


    ENABLE_GPIOA_CLOCK();


    if (is_gpioa_clock_enabled()) {

        successful_functions |= 1 << 0;
    } else {

        successful_functions |= 0 << 0;
    }


    set_input_output_mode(1073872896, 1 << 5, 1);


    hardware_abstraction_layer_function_gpio_write_pin(1073872896, 1 << 5, 1);


    if (hardware_abstraction_layer_function_gpio_read_pin(1073872896, 1 << 5)) {

        successful_functions |= 1 << 1;
    } else {

        successful_functions |= 0 << 1;
    }


    hardware_abstraction_layer_function_gpio_toggle_pin(1073872896, 1 << 5);


    if (!hardware_abstraction_layer_function_gpio_read_pin(1073872896, 1 << 5)) {

        successful_functions |= 1 << 2;
    } else {

        successful_functions |= 0 << 2;
    }


    char number_str[12];
    int_to_string(successful_functions, number_str);


    print(number_str);



    while (1);

    return 0;
}
