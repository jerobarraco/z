; Declare some external functions
;
extern	printf		; the C function, to be called
SECTION .data		; Data section, initialized variables
a:	dd	5		; int a=5;
fmt:    db "a=%d, eax=%d", 10, 0 ; The printf format, "\n",'0'
	section .text ; ; code goes here
	global main ; ;entry point
_start:
main:
	push    ebp		; set up stack frame
	mov ebp, esp
	mov eax, [a]
	add	eax, 2		; a+2
		push DWORD eax ;param
		push DWORD [a] ;param
		push DWORD fmt ;param
	call printf
	add esp, 12 ;return
	mov     esp, ebp	; takedown stack frame
	pop     ebp		; same as "leave" op
	;exiting!
	mov eax, 1
	mov ebx, 0
	int 80h  ;byebyecruelworld
	

