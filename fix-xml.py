import os, re, time

start_time = time.time()
print("Replacing bad XML chars in files")
for file in os.listdir(os.fsencode("./")):
	filename = os.fsdecode(file)
	if filename.endswith(".xml"):
		print("    " + filename)

		# Open file
		fin = open(filename, "rt")
		data = fin.read()
		fin.close()

		# Replace bad XML chars
		data = data.replace('&#x2;', '(')
		data = data.replace('&#x3;', ')')
		illegal_xml_re = re.compile(u'[\x00-\x08\x0b-\x1f\x7f-\x84\x86-\x9f\ud800-\udfff\ufdd0-\ufddf\ufffe-\uffff]')
		data = illegal_xml_re.sub('', data)

		# Write fixed file
		fout = open(filename, "wt")
		fout.write(data)
		fout.close()

print("Finished after %ss!" % round(time.time() - start_time, 2))
