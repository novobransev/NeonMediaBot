string = '   8.18MiB'
number = float(string.split('M')[0].strip())
integer = int(number)

print(integer)