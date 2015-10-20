Only loop necessary is for.
Most normal loops needs an initialization, a break condition and a modification to the control var.
That's better for programmers. Is good when they're learning because it makes them realize what's impoartant.
And is even more important for seasoned developers as they tend to be lazy and do stuff in a weird manner just because they can.

for( <initialization> ; <test> ; <postincrement>):

for (int i = 0; i<10; i++):
	print i
	
Separator:
it could use ,. But that would colide if any of the 3 expressions use it. Like, ie, if i want to create 3 variables in the <initialization>.

Examples:
(Note that pointers are not fixed yet)
## Simple loop

C: 
int i = 0; 
while (i<10){
	something<i>
	i++;
}

C.B:
for(int i = 0; i<10; i++){
	something<i>
}

Z: 
for(int i = 0; i<10; i++):
	something<i>
	
	
## Condition based loop
C: 
struct node *p = list;
while(p!=NULL){
	something<p>
	p = p->next;
}

CB: 
for(struct node p = list; node!=NULL; node = node->next){
	something<p>
}

Z:
for(node p = list; p != None; p = p.next):
	something<p>
	
## "But i need a while"-excuse loop
c: 
impossiburu
you need an initialization,
you need a break condition
you need to transform the variable

but lets assume you don't
while(true){
	something
	something
	break;
}

you could simply write
bool flag = true;
while (flag){
	something
	flag = false;
	break;
}

z:
for(bool flag=True; flag; ):
	something
		flag = False;

Any way you can always skip the <initialization> and or <postincrement> statements
for(;true;):
	something
		break;
		
#All-in-one
c:
while(q = read()){
	something<q>
}     

z: 
for (;q=read();):
	something<q>
	
Im not actually sure to include this kind of side-effect (assignment on evaluation)