	* Change to 64b
	Z Compiler in Z
	Z Compiler in Python
		Better stream reader
			* endline and tab managment. 
				* Consume func (handle depletion, level, and in-place-strip)
				* scan
				* strip
				* level
				* sorted by len scan
			auto section
				needs global admin
			new flow
				0) Have one GLOBAL admin to request stuff (var creation, var info, block info, etc)
				1) change multiline expressions to oneliners
					(strings, parenthesis, enums, math)
				2) divide blocks
				3) parse block identifier
				4) Mark module as loaded, import other modules
				3) parse blocks
				4) asm-fi
				
		* COMMENTS!!!! (one liners at least)
		Instructions
			!!! Types are a mess
				treat all types the SAME (like all literals and such)
			pe)
				The @ and # create a new ident
				we need the global admin for this
	
			* Literas (only numbers)
			Literals (strings or chars) (needs _global admin_ to create vars outside block)
				char 
				arrays (strings)
			
			* Variables
			Expressions
				* Assignment
					Assign to the same register
				* Boolean (for ifs)
				* push
				* pop
				result_in
				Math
					* Add, Sub, Div, Mod, inc/dec, Mul
				Bool
					not, and, or, xor
				var_size (needs global)
				Multiple expressions (ie if func()==3)
			Functions
				* definition
				calling
					* basic
					Arguments
						* detect
						* pass
						pass less than 8Bytes
						param name
					return values
			* Branch
				* If
				Compare two memories (see asign mem2mem)
			* Loops
				* While (nobody needs a while when there's a for)
				* for
				foritch (foreach)
		Struct
			Types
			data structures
			metainfo
		Const
			data types
		Namespaces (honk honk cheeen)
			imports