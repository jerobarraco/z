section .bss
;segment readable
;segment writeable
buffer: resb 2048 ; A 2 KB byte buffer used for read
section .data
;segment readable;this will cause sigsev
;segment writeable
entero: dq 5
hFile: dq 0
hFileName: dq 0
readed: dq 0
buflen: dq 2048
saludo: db 'Bienvenidos a el compilador Z, por favor llame con el nombre de archivo *.z a parsear',0
saludoLen: dd 89
	section .text ; code goes here
	global main ; entry point
_start:
main:
	;  rdi = argc
	;  rsi = argv[]
	cmp QWORD rdi, 1
	jnl _if_end_140131397025920 ; jump to false, below is 'true'
		call exit
	_if_end_140131397025920:
	mov rax, [rsi+8] ; expand mem2mem mov
	mov [hFileName], rax
		mov rdi, [hFileName] ; 'open' reg param 0
	call open
	mov [hFile], rax ; store previous result
	;  exit(int 0)
	cmp QWORD [hFile], 01
	jl _if_end_140131397077704 ; jump to false, below is 'true'
			mov rdi, [hFile] ; 'read' reg param 0
			mov rsi, buffer ; 'read' reg param 1
			mov rdx, [buflen] ; 'read' reg param 2
		call read
		mov [readed], rax ; store previous result
			nop
		_forstart_140131397141000:
			cmp QWORD [readed], 0
			jng _forend_140131397141000 ; jump to false, below is 'true'
				mov rdi, [readed] ; 'print' reg param 0
				mov rsi, buffer ; 'print' reg param 1
			call print
				mov rdi, [hFile] ; 'read' reg param 0
				mov rsi, buffer ; 'read' reg param 1
				mov rdx, [buflen] ; 'read' reg param 2
			call read
			mov [readed], rax ; store previous result
			jmp _forstart_140131397141000
		_forend_140131397141000:
	_if_end_140131397077704:
	; 	close(int hFile)
	; exiting!
	mov eax, 60
	mov rdi, 0
	syscall
	

;  now with 100% more comments
open:
	;  open(char *path, int flags, mode_t mode) put filename in ebx. return is on eax
	;  rax = 2, rdi = filename, rsi = O_WRONLY, rdx =flags for create
	;  rdi = @+4 fname is already on rdi
	mov rax, 2
	mov rsi, 0
	mov rdx, 0
	syscall
	ret ; ; end open

close:
	;  rdi = @+4 first param is already rdi
	mov rax, 3
	syscall
	ret ; ; end close

print:
	mov rax, 1
	;  len to syscall len
	mov rdx, rdi
	mov rdi, 1
	;  rsi is first param no need to change
	syscall
	ret ; ; end print

read:
	;  read(int fd, void *buf, size_t count);;fd=rdi, buf=rsi, len=rdx; ret=rax
	mov rax, 0
	syscall
	ret ; ; end read

exit:
	mov rax, 60
	;  rdi = 0 · param already on rdi
	syscall
	ret ; ; end exit

