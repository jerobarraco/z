section .bss
buffer: resb 2048 ; A 2 KB byte buffer used for read
section .data
saludo: db 'Welcome to Z!',10,0
saludoLen: dd 20
	section .text ; code goes here
	global main ; entry point
_start:
main:
		mov rdi, [saludoLen] ; 'print' reg param 0
		mov rsi, saludo ; 'print' reg param 1
	mov rax, 0 ; xmm registers
	call print
	; exiting!
	mov eax, 60
	mov rdi, 0
	syscall
	

print:
	mov rax, 1
	;  len to syscall len
	mov rdx, rdi
	mov rdi, 1
	;  rsi is first param no need to change
	syscall
	ret ; ; end print

