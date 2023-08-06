#!/usr/bin/python3




from pypine import *
import pypinex_pack as pack




tasks = Tasks()





tasks.add("demo", "A demonstration PyPine script for packing with uploadpack.", [
		core.src(".", "hello_world.txt"),
		pack.compressUP("foo.up.gz"),
		core.cat(),
	]
)




tasks.run("demo")






