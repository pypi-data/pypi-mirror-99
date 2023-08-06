#!/usr/bin/python3




from pypine import *
import pypinex_pack as pack




tasks = Tasks()





tasks.add("demo", "A demonstration PyPine script for packing with uploadpack.", [
		pack.createUP("foo.up.gz"),
		core.sequence(
			core.constructChain(
				core.src(".", "hello_world.txt"),
				pack.addToUP("foo"),
			),
			core.constructChain(
				core.src(".", "the_quick.txt"),
				pack.addToUP("bar"),
			),
		),
		pack.closeUP(),
		core.cat(),
		core.echo(),
	]
)



tasks.getE("demo").dump()
tasks.run("demo")






