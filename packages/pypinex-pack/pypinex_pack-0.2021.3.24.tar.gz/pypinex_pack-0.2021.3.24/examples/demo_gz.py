#!/usr/bin/python3




from pypine import *
import pypinex_pack as pack




tasks = Tasks()





tasks.add("demo", "A demonstration PyPine script for packing with gzip.", [
		core.src(".", "hello_world.txt"),
		pack.gzip(),
		core.cat(),
		pack.gunzip(),
		core.echo(),
	]
)




tasks.run("demo")






