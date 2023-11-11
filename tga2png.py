import os

folders = ["tga", "png"]

for i in folders:
	if not os.path.exists(f"./{i}"):
		os.makedirs(f"./{i}")
	
for f in os.listdir("./tga/"):
	if f.endswith(".tga") or f.endswith(".tga__alpha"):
		filename = os.path.basename(f)
		tga = open(f"./tga/{filename}", "rb")
		#Getting compressed data offset
		compressed_offset = tga.read().find(b"\x26\xb5")
		#PVR Header
		tga.seek(0)
		pvr_header = tga.read(compressed_offset)
		#Compression Info
		tga.seek(52)
		compression = tga.read(4)
		if compression == b"zstd":
			try:
				tga.seek(compressed_offset)
				compressed_data = tga.read()
				#Saving
				if filename.endswith(".tga"):
					outfile = f"png/{filename[:-4]}"
				else:
					outfile = f"png/{filename[:-11]}__alpha"
				decompressed_data = open(f"{outfile}_compressed.pvr", "wb")
				decompressed_data.write(compressed_data)
				decompressed_data.close()
				os.system(f"zstd -d {outfile}_compressed.pvr -o {outfile}.pvr -f") #libraries doesnt work
				decompressed_data = open(f"{outfile}.pvr", "rb").read()
				decompressed_file = open(f"{outfile}.pvr", "wb")
				decompressed_file.write(pvr_header+decompressed_data)
				decompressed_file.close()
				print(f"Succesfully decompressed {filename}!")
				os.system(f'PVRTexToolCLI.exe -i "{outfile}.pvr" -d "{outfile}.png" -noout -ics srgb -f etc1,ubn,srgb')
				os.remove(f"{outfile}_compressed.pvr")
				os.remove(f"{outfile}.pvr")
			except Exception as e:
				print(f"Cant decompress {filename}! Error: {e}")
				pass
		else:
			print(f"Unsupported compression({compression})")