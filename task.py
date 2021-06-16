
from collections import OrderedDict

class MempoolTransaction():
    
    def __init__(self, txid, fee, weight, parents, *args):
        self.txid = txid
        self.fee = int(fee)
        self.weight = int(weight)
        
        self.parents = [];
        if parents != '':
            self.parents.append(parents)
        
        for par in args :                              # I am using args to get the parent txids which will send the rest of the arguments to the *args
            if par != '':                               # which I append it to the Parents list
                self.parents.append(par)

        # TODO: add code to parse weight and parents fields
    
    def show_data(self):                                  # showing the object data recieved 
        print(self.txid)
        print(self.fee)
        print(self.weight)
        print(self.parents)



def parse_mempool_csv():
    """Parse the CSV file and return a list of MempoolTransactions."""
    with open('./mempool.csv') as f:
        lines = f.readlines()[1:]
        return ([MempoolTransaction(*line.strip().split(',')) for line in lines])
    f.close()


def contruct_dict(objectData):
    objectIndexdict = OrderedDict()                             # made a ordered dictionary to store the index of each transaction ids
    for idx,obj in enumerate(objectData):
        objectIndexdict[obj.txid] = idx;
    return objectIndexdict
    """ for key, value in objectIndexdict.items():
        print(key + " = " + str(value)) """


def transations_with_no_parent(objectData):                         # Separated the Transactions which have no parent
    transactionsList = []
    for obj in objectData:
        if len(obj.parents) == 0:       
            transactionsList.append(obj);               
    """ for obj in transactionsList: 
        obj.show_data() """
    
    return transactionsList

def valid_transations_with_parent(objectData, objectIndDict):               #  Separated the Valid Transaction which have one or more parent
    validTransactionsList = []                                               # I get through the Ordered Dict made above
    for obj in objectData:
        if len(obj.parents) > 0:
            c = 0
            for parId in obj.parents:                                         # if each of the parent txid comes before the index of the transaction then I increase the count 
                if objectIndDict.get(obj.txid) > objectIndDict.get(parId):          
                    c = c + 1                                                        # finally if the count is equal to the number of parents then the transaction is valid
                else:
                    break
            if c == len(obj.parents):
                validTransactionsList.append(obj);
    """ for obj in validTransactionsList: 
        obj.show_data()  """
    
    return validTransactionsList

def contruct_ind_dict(objectData):        # Ordered Dict used to store the txid against index
    indexObjectdict = OrderedDict()
    for idx,obj in enumerate(objectData):
        indexObjectdict[idx] = obj.txid;
    return indexObjectdict

def arrayList(objectData,prop):  # used for extracting data of specific type
    dataList = []
    for obj in objectData:
        dataList.append(getattr(obj, prop))
    return dataList

def largestContiguousSubArray(wt , fees, objectIndDict):     # largest contiguous subarray that has maximum weight less than maximum block weight
    
    objectIncludedInTheBlock=[]
    present_sum =present_wt =ini_index =fin_index =maxPossibleFee =start =weight =end = 0

    for i in range(len(fees)):

        if present_wt + wt[i] <= maximumBlockWt: 
            present_wt += wt[i]                                 
            present_sum += fees[i]
            fin_index += 1 
        else:
            present_wt -= wt[ini_index]                                   
            present_sum -= fees[ini_index]
            ini_index += 1                                                         
            
            if present_wt+wt[i] <= maximumBlockWt:
                present_wt += wt[i]                                   
                present_sum += fees[i]
                fin_index += 1
            if present_sum > maxPossibleFee  and present_wt <= maximumBlockWt:
                maxPossibleFee  = present_sum
                start = ini_index
                end = fin_index
                weight = present_wt
    
    print("Maximum Possible Fee Gained By the Miner", maxPossibleFee)
    print("Start Index of the Contiguous Array",start)
    print("End Index of the Contiguous Array",end)
    print("Max weight attained By the block", weight)
    
    for i in range(start,end+1):
        objectIncludedInTheBlock.append(objectIndDict[i])
    return objectIncludedInTheBlock


objectData = parse_mempool_csv()
maximumBlockWt = 4000000
objectIndDict = contruct_dict(objectData)

transactionsListWithNoParent = transations_with_no_parent(objectData)

validTransactionListWithParent = valid_transations_with_parent(objectData, objectIndDict)

validTransactionListWithAllData = transactionsListWithNoParent + validTransactionListWithParent

print("Valid Transactions with No Parent :", len(transactionsListWithNoParent))
print("Valid Transactions with Parent :", len(validTransactionListWithParent))
print("All Valid Transactions :", len(validTransactionListWithAllData))

newIndexedObjectIdDict = contruct_ind_dict(validTransactionListWithAllData)

feesList = arrayList(validTransactionListWithAllData,"fee")
weightList = arrayList(validTransactionListWithAllData,"weight")
objectIncludedInTheBlock = largestContiguousSubArray(weightList, feesList, newIndexedObjectIdDict)
print("Final Objects Included in the block are :", len(objectIncludedInTheBlock))
outputFile = open("block.txt", "w")
with open('block.txt', 'w') as f:
    for item in objectIncludedInTheBlock:
        f.write("%s\n" % item)
    f.close()
