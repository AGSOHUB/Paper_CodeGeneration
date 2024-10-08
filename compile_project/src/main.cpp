#include "stm32f4xx.h"
#include <stm32f4xx_rcc.h>
#include <stm32f4xx_usart.h>

extern "C" int main()
{
  // Switch on blue LED on STM32F407Discovery

  RCC_AHB1PeriphClockCmd(RCC_APB1Periph_USART2, ENABLE);
  USART_ClockInitTypeDef USART_ClockInitStruct;
  USART_ClockStructInit(&USART_ClockInitStruct);
  USART_ClockInit(USART2,&USART_ClockInitStruct);
  USART_InitTypeDef USART_InitStruct;
  USART_StructInit(&USART_InitStruct);
  USART_Init(USART2,&USART_InitStruct);
  char data[13] = "Hello World!";
  for (int i=0; i<13 ; i++){
    USART_SendData(USART2,(uint16_t) data[i]);
  }
  
  for (;;);

  return 0;
}
