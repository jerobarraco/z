; printf1.asm   print an integer from storage and from a register
; Assemble:	nasm -f elf -l printf.lst  printf1.asm
; Link:		gcc -o printf1  printf1.o
; Run:		printf1
; Output:	a=5, eax=7
; Equivalent C code
; /* printf1.c  print an int and an expression */
; #include 
; int main()
; {
;   int a=5;
;   printf("a=%d, eax=%d\n", a, a+2);
;   return 0;
; }
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
	mov     ebp,esp
	mov	eax, [a]	; put a from store into register
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
	

