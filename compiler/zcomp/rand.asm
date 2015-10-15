; Declare some external functions
;
extern	rand		; the C function, to be called
extern printf
extern srand
extern time
extern scanf
extern fopen
extern strlen
SECTION .data		; Data section, initialized variables
a:	dd	5		; int a=5;
fmt:    db "num=%d", 10, 0 ; The printf format, "\n",'0'
mensaje: db 'how long is this?',0
mensajeLen: dd 17
lectura: db '%d',0
lecturaLen: dd 2
num: dd 0
	section .text ; ; code goes here
	global main ; ;entry point
_start:
main:
	 ; "opens" a file (does nothing but doesn't crash)
		push DWORD 0 ;param
	call fopen
	add esp, 4 ;return
	 ; get current time
		push DWORD 0 ;param
	call time
	add esp, 4 ;return
	 ; seeds random
		push DWORD eax ;param
	call srand
	add esp, 4 ;return
	 ; gets one random number
	call rand
	 ; shows it
		push DWORD eax ;param
		push DWORD fmt ;param
	call printf
	add esp, 8 ;return
	 ; read and echo a number
		push DWORD num ;param
		push DWORD lectura ;param
	call scanf
	add esp, 8 ;return
		push DWORD [num] ;param
		push DWORD fmt ;param
	call printf
	add esp, 8 ;return
	 ;get string length
		push DWORD mensaje ;param
	call strlen
	add esp, 4 ;return
		push DWORD eax ;param
		push DWORD fmt ;param
	call printf
	add esp, 8 ;return
	;exiting!
	mov eax, 1
	mov ebx, 0
	int 80h  ;byebyecruelworld
	

