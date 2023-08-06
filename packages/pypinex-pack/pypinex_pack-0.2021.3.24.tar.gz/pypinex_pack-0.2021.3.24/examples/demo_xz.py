#!/usr/bin/python3




from pypine import *
import pypinex_pack as pack




tasks = Tasks()





tasks.add("demo", "A demonstration PyPine script for packing with xz.", [
		core.src(".", "hello_world.txt"),
		pack.xz(),
		core.cat(),
		pack.unxz(),
		core.echo(),
	]
)




tasks.run("demo")






