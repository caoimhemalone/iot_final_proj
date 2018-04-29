import dweepy

thingName="CaoimhesIotFinalThing";

for dweet in dweepy.listen_for_dweets_from('CaoimhesIotFinalThing'):
	print dweet