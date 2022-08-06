def my_sort(line):
    line_fields = line.strip().split(',')
    amount = line_fields[0]
    return amount
  
  
# opening file MallSalesData.csv
# and getting contents into a list
fp = open("C:\\Users\\Ethan\\Documents\\VSCODE\\combined.txt")
contents = fp.readlines()
  
# sorting using our custom logic
contents.sort(key=my_sort)

np = open('new.txt', 'w')
# printing the sorting contents to stdout
for line in contents:
    print(line)
    np.write(line)
fp.close()