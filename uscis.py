from main import *

url_nm2_buy=  'https://egov.uscis.gov/casestatus/landing.do'  
rec_num1='src'
num=2090100000
case_485='I-485,' 
final_list=[] 
first = True   

web1 = UscisOp1(url_nm2_buy)
      
for num in range(num, num+10000, 1):
    rec_num= rec_num1 + str(num)
    if first:
        try:
            print("running for the first time")
            click_1=web1.en_n_clk_1(rec_num)
        except (ElementNotInteractableException): 
            print("inside exception")
            web1.close_error()    
 

        print ("first in before is ",first)
        first = False
        print ("first in after is",first)
    else:
        try:
            print("running for the 2nd time")
            click_1=web1.en_n_clk_2(rec_num) 
            print ("second in ",first)
        except (ElementNotInteractableException): 
            print("inside exception 2nd run ")
            web1.close_error()       
    case_text=web1.get_case()
    status_text=web1.get_status()
    print (case_text)
    l_date=list(datefinder.find_dates(case_text))
      
    #print(l_date[0])
    #print(case_text)
    #web2.close_conn()   
    #//*[@id="receipt_number"]
    #//*[@id="receipt_number"]
    #/html/body/div[2]/form/div/div[1]/div/div/div[2]/div[3]/h1
    #/html/body/div[2]/form/div/div[1]/div/div/div[2]/div[3]/p

    if (isWordPresent(case_text,case_485)):
        print("This is I_485 case")
        #print (rec_num)

        #print (status_text)
        final_list.append(case_485)
        final_list.append(rec_num)
        final_list.append(status_text)
        final_list.append(l_date[0])
        
        print(final_list)
        #web1.close_conn()
    else:
        print("No")
        #web1.close_conn()
web1.close_conn()
new_list = [final_list[i:i+4] for i in range(0, len(final_list), 4)]
#for i in range(0, len(final_list), 4):
# print(*final_list[i:i+4], sep='      ')  
df = DataFrame (new_list,columns=['case_type','receipt_num','status','last_date'])
#df = DataFrame (final_list,columns=['case_type'])

print (df)
df.to_excel('uscisscan_10k.xlsx')

web1.send_email("kdasra276@gmail.com", "Krishna1@","dasra23@gmail.com","content here ","uscisscan_10k.xlsx","Test email")
