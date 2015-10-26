section .bss
segment readable
segment writeable
buffer: resb 2048 ; A 2 KB byte buffer used for read
section .data
segment readable
;segment writeable
entero: dd 5
hFile: dq 0
hFileName: dq 0
readed: dd 0
buflen: dd 2048
saludo: db 'Bienvenidos a el compilador Z, por favor llame con el nombre de archivo *.z a parsear',0
saludoLen: dd 89
	section .text ; ; code goes here
	global main ; ;entry point
_start:
main:
	 ; rdi = argc
	 ; rsi = argv[]
	cmp QWORD rdi, 1
	jnl _if_end_139871549644528 ;jump to false, below is 'true'
		call exit
	_if_end_139871549644528:
	 ;ecx = @+4
	 ;edx = @+8
	 ;eax = @edx+4
	mov [hFileName], eax
mov rdi, [hFileName]
call open
	mov [hFile], rax
	mov rdi, [hFile]
	call close
	 ;if hFile >= 01:
	 ;	readed = read(int hFile, str buffer, int buflen)
	 ;	for eax=0 ; readed > 0; readed = read(int hFile, str buffer, int buflen):
	 ;		print(str buffer, int readed)
	 ;	close(int hFile)
	; exiting!
	mov eax, 60
	mov rdi, 0
	syscall
	

 ; now with 100% more comments
open:
	 ; open(char *path, int flags, mode_t mode) put filename in ebx. return is on eax
	 ; rax = 2, rdi = filename, rsi = O_WRONLY, rdx =flags for create
	 ; rdi = @+4 fname is already on rdi
	mov rax, 2
	mov rsi, 0
	mov rdx, 0
	syscall
	ret ;; end open

close:
	 ; rdi = @+4 first param is already rdi
	mov rax, 3
	syscall
	ret ;; end close

print:
	mov ecx, [rsp+4]
	mov edx, [rsp+8]
	mov eax, 4
	mov ebx, 1
	syscall
	ret ;; end print

read:
	 ; read(int fd, void *buf, size_t count);;fd=ebx, buf=ecx, len=edx; ret=eax
	mov ebx, [rsp+4]
	mov ecx, [rsp+8]
	mov edx, [rsp+12]
	mov eax, 3
	syscall
	ret ;; end read

exit:
	mov rax, 60
	mov rdi, 0
	syscall
	ret ;; end exit

