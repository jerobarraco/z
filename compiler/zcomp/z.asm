section .bss
buffer: resb 2048 ; A 2 KB byte buffer used for read
section .data
entero: dd 5
hFile: dd 0
hFileName: dd 0
readed: dd 0
buflen: dd 2048
saludo: db 'Bienvenidos a el compilador Z, por favor llame con el nombre de archivo *.z a parsear',0
saludoLen: dd 89
	section .text ; ; code goes here
	global main ; ;entry point
_start:
main:
	mov ecx, [esp+4]
	mov edx, [esp+8]
	mov eax, [edx+4]
	mov [hFileName], eax
		push DWORD [hFileName] ;open_r param 0
	call open_r
	add esp, 4 ;end open_r
	cmp eax, 01
	jl _if_else_139686860205304 ;jump to true, below must be jmp to false
		mov [hFile], eax
			push DWORD [buflen] ;read param 0
			push DWORD buffer ;read param 1
			push DWORD [hFile] ;read param 2
		call read
		add esp, 12 ;end read
			nop
		_forstart_139686860207048:
			cmp eax, 0
			jng _forend_139686860207048 ;jump to true, below must be jmp to false
			mov [readed], eax
				push DWORD [readed] ;print param 0
				push DWORD buffer ;print param 1
			call print
			add esp, 8 ;end print
				push DWORD [buflen] ;read param 0
				push DWORD buffer ;read param 1
				push DWORD [hFile] ;read param 2
			call read
			add esp, 12 ;end read
			jmp _forstart_139686860207048
		_forend_139686860207048:
	jmp _if_end_139686860205304
	_if_else_139686860205304:
	_if_end_139686860205304:
	;exiting!
	mov eax, 1
	mov ebx, 0
	int 80h  ;byebyecruelworld
	

 ; now with 100% more comments
open_r:
	 ; open(char *path, int flags, mode_t mode) put filename in ebx. return is on eax
	mov ebx, [esp+4]
	mov eax, 5
	mov ecx, 0
	mov edx, 0
	int 128
	ret ;; end open_r

print:
	mov ecx, [esp+4]
	mov edx, [esp+8]
	mov eax, 4
	mov ebx, 1
	int 128
	ret ;; end print

read:
	 ; read(int fd, void *buf, size_t count);;fd=ebx, buf=ecx, len=edx; ret=eax
	mov ebx, [esp+4]
	mov ecx, [esp+8]
	mov edx, [esp+12]
	mov eax, 3
	int 128
	ret ;; end read

