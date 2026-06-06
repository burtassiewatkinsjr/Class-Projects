#@Author Burtassie Watkins


from math import trunc
import os
from random import randint
from multiprocessing import *


#master-START
def info(title):
    print (title)
    print ('module name:', __name__)
    if hasattr(os, 'getppid'):  # only available on Unix

        #(Organization) print process ID child is -.getppid()
        print ('process ID:', os.getppid())
    else:
        print ("I'm a parent")    
    #(Organization) print parent process ID parent is -.getpid()
    print ('Parent process id:', os.getpid())
#master-END


#(slave Process)-START
def slave(totalWork,list,list_size,start,queue):

    summ=0 #variable
    
    #(loop)-START__ counts up all numbers within the totalWork
    for x in range (start,totalWork):
        summ=summ+list[start]      
        start=start+1 
        #(Debbug output) if statment
        if (start==totalWork):
                
                info('Child')
                print(" sum: ", summ, " Amount of work completed: " ,round(((((start)/list_size))*100),2),"%")
                queue.put(summ)
    #(loop)-END                
#(slave Process)-END                    
                
            
#(array funtion)START
def array(n):
    randomList=[] #empty array
    #This is new
    if 1000 % n != 0:
         for i in range((1000 % n)):
            randomList = [(randint(0, 1000)) for i in range(int(1000 / n))]

    #creating array of n elements with random numbers 0-9999
    for i in range(n):
        randomList.append(randint(0,9999))
    return(randomList)          
#(array funtion)END    
    



#(main line)START
if __name__ == '__main__':
    info('main line')
    queue=Queue()

    #(Variables)
    array_size =1000
    start_point=0
    List_of_nums=array(array_size) #(array Function)
    print(List_of_nums)
    number_of_processes=int(input("How many worker processes will you want to use today: "))
    workers=number_of_processes

    #(security)if statment
    if(number_of_processes!=0):
        load_size=array_size/number_of_processes #amount of work each process will do
        high=trunc(load_size)#(secrity) setting load_size to a whole number

    total_summ=0 #(variable)
    #(security)loop
    while (number_of_processes>((array_size/2)+1)):
        print("You have too many processes for the amount of work. Try A number ( 1-",((array_size/2)+1)," )")
        number_of_processes=int(input("How many worker processes will you want to use today: "))
        workers=number_of_processes
        load_size=array_size/number_of_processes #amount of work each process will do
        #high=trunc(load_size)#(secrity) setting load_size to a whole number
        
    
    #(looping)START- Creating the number of processes the user asked for
    for x in range (number_of_processes):
         #cross communication for processes
         queue=Queue()
         #creating a new process
         p = Process(target=slave, args=(trunc(high),List_of_nums,array_size,start_point,queue))
         
         
         #start a new process
         p.start()  

         #(update) passing new value to variables in the list 
         total_summ=total_summ+queue.get()
         start_point=start_point+trunc(load_size)
         high=high+trunc(load_size)
         workers=workers-1  

         #(Security)- last worker accounts for rest of the elements
         if (workers==1):
              high=array_size

         #(Organization) when we have large number of processes they need to print in order 
         if (workers==0):   
            p.join()  
            info('main')
            print("Total Sum: ",total_summ)

    #(loop)END
#(main line) END
