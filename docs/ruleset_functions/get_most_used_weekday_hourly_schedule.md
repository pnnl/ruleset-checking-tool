# get_most_used_weekday_hourly_schedule

**Description:** Get the most used weekday hourly schedule from an annual 8760 schedule as list of hourly values for a 24 hour period.

**Inputs:**  
- **B-RMD,P-RMI**: To calculate the the most used weekday hourly schedule from an annual 8760 schedule.   
- **RMD**: To obtain the data elements associated with the Calendar object (day of week for Jan 1st, is leap year, and has daylight savings time). 
- **schedule_obj**: The schedule object sent to this function.  

**Returns:**  
- **get_most_used_weekday_hourly_schedule**: The function calculates and returns the most used weekday hourly schedule from an annual 8760 schedule as list of hourly values for a 24 hour period (Not looking for average just looking for the most common schedule used on the weekdays in a year, even minor differences in schedules make the schedules considered different, this should be based on 24 hourly values (not just the sum across the day)). Count the number of unique weekday schedules and the one that is used the most times is the winner.
 
**Function Call:**  None

## Logic:    
To be developed by RCT team. Need the function to return the list of hourly values as described above.  

**Returns** `get_most_used_weekday_hourly_schedule`  

**Questions:**  
1. Is there a way to get the RMD objects from the rulesetmodel instances? In other words is it necessary to send both to this function?

**[Back](../_toc.md)**
