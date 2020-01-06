#Prime Density Finder
import math, random, timeit, time, datetime, csv

def isPrime(n):
    if n == 1:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    w = 2

    while i * i <= n:
        if n % i == 0:
            return False

        i += w
        w = 6 - w

    return True
    
def main():
    print("-------------------------\n{:^25}\n-------------------------\n".format("PRIME-TIME"))
    
    #Take inputs to populate data structures
    firstBits = int(input("How many bits shall the first random number have?\n"))
    lastBits = int(input("How many bits shall the last random number have?\n"))
    numOfRands = int(input("How many random numbers shall we generate per bit?\n" + 
                           "This will be scaled to the ceiling of bit length\n"))
    distance = int(input("How much farther from the random number shall we look for a prime?\n"))
      
    #Initialise dictionaries
    now = datetime.datetime.now()
    fileName = now.strftime("%a, %d %b %Y %H %M %S")
    bitsDictionary = {}
    totalsDictionary = {}
    fieldNames = ['Bit',
                  'Number of Randoms',
                  'Total Primes',
                  'Time Taken',
                  'Primes Per Thousand',
                  'Local Time',
                  'Expected Primes Per Thousand']
    total = 0
    run = 0
    totalRuns = 0
    
    #Values are being stored by their total bits, then grouped.
    for bits in range(firstBits, lastBits+1):
        
        bitsDictionary[bits] = {}
        totalsDictionary[bits] = 0
        
        #Ensuring we don't have fewer entries in our dictionary,
        #as confined by maximum interger representation for bit length
        
        while ((len(bitsDictionary[bits]) < numOfRands) and
               (len(bitsDictionary[bits]) < 2**bits)): 
            randomNum = random.getrandbits(bits)
            if randomNum not in bitsDictionary[bits]:
                bitsDictionary[bits][randomNum] = 0
                totalRuns += 1
    with open('Primes - ' + fileName + '.csv',
              'a',
              newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
        writer.writeheader()
        writer.writerow({'Local Time': time.asctime(time.localtime(time.time()))})
        
        #Get to looking for primes then, lets go ahead and time things.    
        startTime = timeit.default_timer()
     
        for bits in bitsDictionary:
            expected = distance/math.log(2**bits)
            print("Expected number of primes per thousand for " +
                  str(bits) +
                  " bits: " +
                  str(expected))
            bitTime = timeit.default_timer()
            for value in bitsDictionary[bits].keys():
                #Here's where we search the next so many numbers (distance)
                #Possible errors ahead, I've a feeling my averaging is wrong.
                for number in range(value, value+distance+1):
                    if isPrime(number):
                        bitsDictionary[bits][value] += 1
                        
                totalsDictionary[bits] += bitsDictionary[bits][value]
                total += bitsDictionary[bits][value]
                run += 1

            #If we're here, we've finished the checks for this bit, lets store some data
            writer.writerow({'Bit':bits,
                             'Number of Randoms':len(bitsDictionary[bits]),
                             'Total Primes':totalsDictionary[bits],
                             'Time Taken': timeit.default_timer() - bitTime,
                             'Primes Per Thousand':(totalsDictionary[bits]/len(bitsDictionary[bits])),
                             'Expected Primes Per Thousand':expected})
            
            #And output to terminal so we know it's not crashed
            thisonestime = timeit.default_timer() - bitTime
            print("Bit " +
                  str(bits) +
                  " took " +
                  (str(thisonestime)) +
                  " seconds")
            print("We found " +
                  str((totalsDictionary[bits]/len(bitsDictionary[bits]))) +
                  " primes per thousand at this bit level")
            print(str(timeit.default_timer() - startTime) +
                          " seconds have elapsed")
            print("It is expected to take: " +
                  str(thisonestime*1.5) +
                  " seconds to get the next batch done\n")
            print("End Time is " + str(time.asctime(time.localtime(time.time()))))

        #If we hit here, we're done. Lets log the finish time and output some more info    
        print("Run total: " +
              str(run))
        print("Average Primes Found: " +
              str(total/run))
        print("It took: " +
              str(timeit.default_timer() - startTime) +
              " seconds to work this out")

if __name__ == '__main__':
    main()
