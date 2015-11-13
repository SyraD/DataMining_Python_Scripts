all_ids = self.session.query(ACCOUNT).all()
        
for i in all_ids[0:]:   #use the number in quotation to assign starting ID #you need to create a table named "accounts" in Sqlite DB and define tables used in the following block of code. 
    Unique_ID = i.Unique_ID
    Twitter_handle = i.Twitter_handle
    kid = Twitter_handle     			
    rowid = i.Unique_ID
    party_code = i.party_code

    print '\n', "\rprocessing id %s/%s  --  %s" % (rowid, len(all_ids), Twitter_handle),
    sys.stdout.flush()     
            
    page = 1

    while page < 1000:
        import time
        time.sleep(15)
        print "------XXXXXX------ STARTING PAGE", page
        d = get_data_user_timeline_all_pages(kid, page)		          
        if not d:
            print "THERE WERE NO STATUSES RETURNED........MOVING TO NEXT ID"
            break	        
        if len(d)==0:    					 
            print "THERE WERE NO STATUSES RETURNED........MOVING TO NEXT ID"
            break
        
        write_data(self, d, Twitter_handle, Unique_ID, party_code)

        #self.session.commit()
        
        #print 'pausing for 1 second'
        #time.sleep(1) #PAUSE FOR 1 SECOND
                    
        page += 1
        if page > 1000:
            print "WE'RE AT THE END OF PAGE 49!!!!!"
            break
    self.session.commit()
                    
print  '\n', '\n', '\n', "FINISHED WITH ALL IDS"
self.session.close()