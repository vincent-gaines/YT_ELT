from datetime import timedelta, datetime

#------------------------------------------------------------------------------------------------------
def parse_duration(duration_str):
    """Parse a duration string contentDetails.duration	string
    The length of the video. The property value is an ISO 8601 duration. For example, for a video 
    that is at least one minute long and less than one hour long, the duration is in the         format PT#M#S, 
    in which the letters PT indicate that the value specifies a period of time, and the letters M and S 
    refer to length in minutes and seconds, respectively. The # characters preceding the M and S letters 
    are both integers that specify the number of minutes (or seconds) of the video. For example, a value 
    of PT15M33S indicates that the video is 15 minutes and 33 seconds long.
    
    If the video is at least one hour long, the duration is in the format PT#H#M#S, in which the # preceding 
    the letter H specifies the length of the video in hours and all of the other details are the same as 
    described above. If the video is at least one day long, the letters P and T are separated, and the 
    value"s format is P#DT#H#M#S. Please refer to the ISO 8601 specification for complete details.
    """
    
    duration_str = duration_str.replace("P", "").replace("T", "")
    
    components = ["D", "H", "M", "S"]
    values = {"D": 0, "H": 0, "M": 0, "S": 0}
    
    
    for component in components:
        if component in duration_str:
            value, duration_str = duration_str.split(component)
            values[component] = int(value)
            
    total_duration = timedelta(days=values["D"], 
                               hours=values["H"], 
                               minutes=values["M"], 
                               seconds=values["S"])
   
    return total_duration

#------------------------------------------------------------------------------------------------------
def transform_data(row):
    """Transform the data by parsing the duration column and adding a new column with the total duration in seconds."""
    
    duration_td = parse_duration(row["Duration"])
    
    row["Duration"] = (datetime.min + duration_td).time()
    
    row["Video_Type"] = "Shorts" if duration_td.total_seconds() <= 60 else "Normal"
    
    return row