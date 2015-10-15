 ;#include <stdio.h>      /* printf */
 ;#include <math.h>       /* pow */
 ;int main (){
 ;  printf ("7 ^ 3 = %f\n", pow (7.0, 3.0) );
 ;  printf ("4.73 ^ 12 = %f\n", pow (4.73, 12.0) );
 ;  printf ("32.01 ^ 1.54 = %f\n", pow (32.01, 1.54) );
 ;  return 0;}
 ;Edit & Run
 ;Output:
 ;7 ^ 3 = 343.000000
 ;4.73 ^ 12 = 125410439.217423
 ;32.01 ^ 1.54 = 208.036691
; Declare some external functions
extern pow		; the C function, to be called
extern printf
extern fopen
SECTION .data		; Data section, initialized variables
ca: db '7 ^ 3 = %f\n',0
caLen: dd 12
cb: db '4.73 ^ 12 = %f\n',0
cbLen: dd 16
cc: db '32.01 ^ 1.54 = %f\n',0
ccLen: dd 19
	section .text ; ; code goes here
	global main ; ;entry point
_start:
main:
		push DWORD 3 ;param
		push DWORD 7 ;param
	call pow
	add esp, 8 ;return
		push DWORD eax ;param
		push DWORD ca ;param
	call printf
	add esp, 8 ;return
	;exiting!
	mov eax, 1
	mov ebx, 0
	int 80h  ;byebyecruelworld
	

