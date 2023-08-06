def Traffic_lights(light):
    """Method that determines the behavior at different traffic lights.
    
    Keyword arguments:
    light -- traffic light color ('green', 'yellow', 'red')
    
    """    
    if light in ["red","yellow"]:
        print("Stop")
    elif light == "green":
        print("Go")
    else:
        print("Entered the wrong word")