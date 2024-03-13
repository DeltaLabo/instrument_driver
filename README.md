## Python pyVISA wrapper library for use with Delta Labs instruments (Rigol DP800, DP700, DL3000)

Before using the library, you need this:

rm = pyvisa.ResourceManager()
res = rm.list_resources()

Identify the resource you are working with and then run this:

instrument = rm.open_resource(res[0])

Keep in mind the index might vary.  You can also just save all the resources to a list and feed the element directly to the parameter, or do whatever you want really.

Then to initialize the instrument object from this wrapper library do this:

Source = controller.Source(instrument)

Replace Source with Load, if it is an electronic load.

Good luck.

Known issues:

- With DP700 series, sometimes queries will fail and crash the program. I just recommed just changing the return line to whatever, or putting it inside a try except. It is not relevant and no one has ever used it, but it's nice to have.

Contact: jairo.rb8@gmail.com
