section .data
hello:     db 'Hello world!',10    ; 'Hello world!' plus a linefeed character
helloLen:  equ $-hello             ; Length of the 'Hello world!' string
hola:		db 'Hola caretas!',10
holaLen:	equ $-hola
global  _start
section .text

_start:
mov ecx,hello        ; Put the offset of hello in ecx
mov edx,helloLen     ; helloLen is a constant, so we don't need to say mov edx,[helloLen] to get it's actual value
int 80h              ; Call the kernel
call imprimir
mov ecx, hola
mov edx, holaLen
nop
call imprimir
nop
;exiting!
mov eax, 1
mov ebx, 0
int 80h;byebyecruelworld



imprimir:
mov eax,4           ; The system call for write (sys_write)
mov ebx,1           ; File descriptor 1 - standard output
int 80h				; enter after the last line is NOT (that) important :)
ret

