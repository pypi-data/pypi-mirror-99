#!/usr/bin/python3




from pypine import *
import pypinex_pack as pack




tasks = Tasks()





tasks.add("demo", "A demonstration PyPine script for packing with bzip2.", [
		core.src(".", "hello_world.txt"),
		pack.bzip2(),
		core.cat(),
		pack.bunzip2(),
		core.echo(),
	]
)




tasks.run("demo")






