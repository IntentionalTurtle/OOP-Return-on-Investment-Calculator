class ROI():
    #set flags, create starter dictionaries, and initialize the main menu
    def __init__ (self):
        self.income = {
                    'rent': 0,
                    'laundry': 0,
                    'storage': 0
                }
        self.expenses = {
                    'taxes': 0,
                    'insurance': 0,
                    'water': 0,
                    'garbage': 0,
                    'electric': 0,
                    'gas': 0,
                    'groundskeeping': 0,
                    'vacancy': 0,
                    'repairs': 0,
                    'capex': 0,
                    'management': 0,
                    'mortgage': 0                
                }
        self.investments = {
            'downpayment': 0,
            'closing costs': 0,
            'rehab budget': 0
        }
        self.income_flag = False
        self.expenses_flag = False
        self.cashflow_flag = False
        self.investment_flag = False
        self.mainMenu()

#central hub which organizes loops of enterInfo() (and dictEdit() inside of that) to update values
#creates a main menu with input decision trees
    def mainMenu(self):
        menu_flag = True
        while menu_flag == True:
            nav = input("\nPlease input the number of the function you would like to do: \n(1) Calculate Income\n(2) Check Income\n(3) Calculate Expenses\n(4) Show Expenses\n(5) Calculate Cash Flow\n(6) Calculate Total Investment\n(7) Cash on Cash Return\nYou may also input 'quit' to exit ROI() ")
            nav = nav.lstrip('(').rstrip(')')
            if nav =='1':
                self.income = self.enterInfo(self.income)
                self.income_flag = True
                self.printDict(self.income)
                print(f'Total Income: {str(sum(self.income.values()))}')
            elif nav == '2':
                self.printDict(self.income)
                print(f'Total Income: {str(sum(self.income.values()))}')
            elif nav == '3': 
                self.expenses = self.enterInfo(self.expenses)
                self.expenses_flag = True
                self.printDict(self.expenses)
                print(f'Total Expenses: {str(sum(self.expenses.values()))}')
            elif nav == '4':
                self.printDict(self.expenses)
                print(f'Total Expenses: {str(sum(self.expenses.values()))}')
            elif nav == '5':
                if self.flagCheck(1,1,0,0) == True:
                    self.cashflow = sum(self.income.values()) - sum(self.expenses.values())
                    self.cashflow_annual = self.cashflow * 12
                    self.cashflow_flag = True
                    print(f'\nMonthly Cashflow: ${self.cashflow}\nAnnual Cashflow: ${self.cashflow_annual}')
            elif nav == '6':
                if self.flagCheck(1,1,1,0) == True:
                    self.investments = self.enterInfo(self.investments)
                    self.investment_flag = True
                    self.printDict(self.investments)
            elif nav == '7':
                if self.flagCheck(1,1,1,1) == True:
                    roi = self.cashflow_annual / sum(self.investments.values()) * 100
                    print(f'\nYour ROI for this property is {roi}% per annum')
            elif nav == 'quit':
                print('\nThank you for using ROI()! Have a nice day!')
                menu_flag = False

#Normalizes string input...specifically with ','s and '$'s in the numbers and extra whitespace. Also converts inputs to integers for use in math
    def fixNum(self, text):
        self.text = text
        text_edited = self.text.replace(',','')
        text_edited = text_edited.strip().lstrip('$')
        return int(text_edited)      

    def printDict(self, dict_a):
        print('\n')
        for key,value in dict_a.items():
            print(f'{key.title()}: ${value}')

#UI tool to confirm changes
    def checkOK(self, a, b):
        ok = input(f'\nAre you sure that {a}: ${str(b)} is correct? Y/N\n')
        if ok.lower() == 'n':
            return False
        if ok.lower() == 'y':
            return True

#gating check to make sure that the correct steps are complete for each portion. a,b,c,d are all just 1s or 0s in main menu
#to activate only the correct checkpoints for a given step.       
    def flagCheck(self, a, b, c, d):
        flags = True
        print('\n')
        if a == 1 and self.income_flag == False:
            print('Calculate Income')
            flags = False
        if b == 1 and self.expenses_flag == False:
            print('Calculate Expenses')
            flags = False
        if c == 1 and self.cashflow_flag == False:
            print('Calculate Cashflow')
            flags = False
        if d == 1 and self.investment_flag == False:
            print('Calculate Investment')
            flags = False
        if flags == False:
            print('\nPlease complete above steps before beginning this step')
            return False
        else:
            return True

#main function which adds or removes key,value pairs to a dictionary
#to edit existing entries, this function called dictEdit()
    def enterInfo(self, info_dict):
        active = True
        while active == True:
            print(f'\nYour current expenses are: ')
            self.printDict(info_dict)
            edit = input("\nWould you like to edit or add a value in the list? Y/N\n")
            if edit.lower() == 'n':
                active = False
                return info_dict
            elif edit.lower() == 'y':
                option = input("\n What would you like to do?\n(1) Edit\n(2) Add New\n(3) Remove\n")
                self.printDict(info_dict)
                entry = input("What is name of the entry you would like to edit, remove, or add to the list? ").lower() 
                if option == str(1) or option.lower() == 'edit':
                    if entry.lower() in info_dict.keys():
                        self.dictEdit(info_dict, entry)
                    else:
                        print("\nThis entry is not already in the list. Please retry using the add command instead.")
                elif option == str(2) or option.lower() == 'add new':
                    amount = self.fixNum(input("\nWhat is the amount for that entry? "))
                    if self.checkOK(entry, amount) == True:
                        info_dict[entry] = amount
                elif option == str(3) or option.lower() == 'remove':
                    rem_sure = input(f'Are you sure you want to remove {entry} and its current value from the list? Y/N\n')
                    if rem_sure.lower() == 'y':
                        del info_dict[entry]
                    if rem_sure.lower() != 'y' and rem_sure.lower() != 'n':
                        print('Invalid Entry. Please try again.')
                else:
                    print("\nInvalid entry. Please make sure to input either the number or phrase of your action without any punctuation.")
            else:
                print('\nPlease enter a Y or N to progress. N will take you back to the main menu.')

    #Used to edit the dictionaries of values if the input key already exist - gives several options to engage with the values to users 
    def dictEdit(self, dict_a, source):
        answer = input("\nWould you like to 'replace' the existing amount, 'add' to the existing amount, or record 'both' sources and amounts separately? (replace/add/both)\n" )
        if answer.lower() == 'replace':
            amount = self.fixNum(input("\nWhat is the new amount for the entry?\n"))
            if self.checkOK(source, amount) == True:
                dict_a[source] = amount
        elif answer.lower() == 'add':
            amount = self.fixNum(input(f"\nHow much would you like to add to the existing value of ${dict_a[source]}?\n"))
            target = dict_a[source] + amount
            if self.checkOK(source, target) == True:
                dict_a[source] += amount
        elif answer.lower() == 'both':
            amount = self.fixNum(input("\nWhat is the amount for the new entry?\n"))
            counter = 1
            source_edited = source
            while source_edited in dict_a.keys():
                source_edited = source + ' ' + str(counter)
                counter += 1
            if self.checkOK(source_edited, amount) == True:
                dict_a[source_edited] = amount
        else: 
            print("\nPlease try again. Make sure to re-enter the category and amount and then you may input 'replace', 'add', or 'both' disregarding the apostrophes.")
        return dict_a                

#diagnostic to run function                               
# ROI()