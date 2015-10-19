	Z Compiler in Z
	Z Compiler in Python
		Better stream reader
			* endline and tab managment. 
				* Consume func (handle depletion, level, and in-place-strip)
				* scan
				* strip
				* level
				* sorted by len scan
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
			* Literas (only numbers)
			Literals (strings or chars) (needs _global admin_ to create vars outside block)
				char 
				arrays (strings)
			* Variables
			Expressions
				* Assignment
				* Boolean (for ifs)
				var size
				result_in
				Math
				push
				pop
				
			Functions
				* definition
				calling
					* basic
					Arguments
						* detect
						* pass
						param name
					return values
			* Branch
				* If
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