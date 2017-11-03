import sys

input_file         = open(sys.argv[1], 'r')
medianvals_by_zip  = open(sys.argv[2], 'w')
medianvals_by_date = open(sys.argv[3], 'w')

# "recipients" maps each CMTE_ID to information about that recipient.
recipients = {}

# An object of type "Recipient" stores information about one recipient.
class Recipient:

	def __init__(self):
	
		# "zips" maps each ZIP_CODE to information about contributions from that zip code.
		self.zips = {}
		
		# "dates" maps each TRANSACTION_DT to information about contributions on that date.
		self.dates = {}

# An object of type "Contributions" stores information about contributions either for a zip code or date.
class Contributions:

	def __init__(self):
	
		# "amounts" is the list of TRANSACTION_AMTs.
		self.amounts = []
		
		# "count" is the total number of all contributions.
		self.count = 0
		
		# "sum" is the sum of all contributions.
		self.sum = 0
		
		# "median" is the median of all contributions.
		self.median = 0
	
	# "insert" is a method to insert a new TRANSACTION_AMT and update all values accordingly.
	def insert(self, amount):
		
		self.amounts.append(amount)
		
		self.count += 1
		
		self.sum += amount
		
		# sort amounts for calculating the new median.
		self.amounts.sort()
		
		if self.count % 2 == 1:
			self.median = self.amounts[self.count/2]
		
		else:
			self.median = round((self.amounts[self.count/2 - 1] + self.amounts[self.count/2]) / 2)

# Process each line/record in input_file...

for line in input_file:
	
	record = line.split('|')
	
	if len(record) < 16:
		continue
	
	CMTE_ID = record[0]
	ZIP_CODE = record[10]
	TRANSACTION_DT = record[13]
	TRANSACTION_AMT = record[14]
	OTHER_ID = record[15]
	
	if len(CMTE_ID) == 0 or len(OTHER_ID) != 0:
		continue
	
	amount = float(TRANSACTION_AMT)
	
	if amount < 200:
		continue
	
	if len(TRANSACTION_DT) == 8 and TRANSACTION_DT.isdigit():
		
		month = int(TRANSACTION_DT[0:2])
		day   = int(TRANSACTION_DT[2:4])
		year  = int(TRANSACTION_DT[4:8])
		
		date = (year * 10000) + (month * 100) + day
		
		recipient = recipients.get(CMTE_ID)
		if recipient is None:
			recipient = Recipient()
			recipients[CMTE_ID] = recipient
		
		contributions = recipient.dates.get(date)
		if contributions is None:
			contributions = Contributions()
			recipient.dates[date] = contributions
		
		contributions.insert(amount)
		
	if len(ZIP_CODE) >= 5 and ZIP_CODE[0:5].isdigit():
		
		zip = int(ZIP_CODE[0:5])
		
		recipient = recipients.get(CMTE_ID)
		if recipient is None:
			recipient = Recipient()
			recipients[CMTE_ID] = recipient
		
		contributions = recipient.zips.get(zip)
		if contributions is None:
			contributions = Contributions()
			recipient.zips[zip] = contributions
		
		contributions.insert(amount)
		
		# Write medianvals_by_zip records in the same order as input file
		medianvals_by_zip.write(CMTE_ID + '|' + ZIP_CODE[0:5] + '|' + str(int(contributions.median)) + '|' + str(contributions.count) + '|' + str(int(contributions.sum)) + '\n')

# Write medianvals_by_date sorted alphabetically by recipient...

recipients_list = recipients.keys()
recipients_list.sort()

for CMTE_ID in recipients_list:
	
	recipient = recipients[CMTE_ID]
	
	if len(recipient.dates) == 0:
		continue
	
	#...and chronologically by date.

	dates_list = recipient.dates.keys()
	dates_list.sort()

	for date in dates_list:
		
		day   = str(date % 100)
		if len(day) == 1:
			day = '0' + day
		month = str((date / 100) % 100)
		if len(month) == 1:
			month = '0' + month
		year  = str(date / 10000)
		
		contributions = recipient.dates[date]

		medianvals_by_date.write(CMTE_ID + '|' + month + day + year + '|' + str(int(contributions.median)) + '|' + str(contributions.count) + '|' + str(int(contributions.sum)) + '\n')

input_file.close()
medianvals_by_zip.close()
medianvals_by_date.close()
