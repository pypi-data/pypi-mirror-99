
space0 = "​"
space1 = "‌"



def hide(text,message):
	message = "".join(format(ord(i),"08b") for i in str(message))
	midpoint = int((len(text)/2)//1)
	result = ""
	for i in list(str(message)):
		result += space0 if i == "0" else space1 if i == "1" else ""
	return text[:midpoint]+result+text[midpoint:]


def show(text):
	result = ""
	for i in list(str(text)):
		if i == space0:
			result += "0"
		elif i == space1:
			result += "1"
	result = "".join([chr(int(result[i:i+8],2)) for i in range(0,len(result),8)])
	if result == "":
		result = None
	return result 

	


