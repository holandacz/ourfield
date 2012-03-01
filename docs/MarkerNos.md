# Place.markerno

    • Places can be added or removed from a territory
    • Place markerno's are numbered from 1 - total markers in the territory boundary
    • They are so numbered to direct volunteer to visit each Place in an efficient order or route.
    • markerno's are dynamic. They may change as Places are added or removed.
    • markerno's are linked to rows of place details in a table view.
    • markerno's are automatically renumbered when new ones are added or existing ones are removed.

Adding new markers
    In ItemEdit, user identifies a target position number. 
    If markerno exists, increment all existing markerno's equal to that number and greater
    If markerno does not exist, no need to alter other markerno's.
    
Moving existing marker
    Get existing markerno
    Get newmarkerno. Must be newmarkerno >= 1 and newmarkerno <= maxmarkerno
    If newmarkerno == oldmarkerno
        no change
    else
        Decrement markernos greater than oldmarkerno and less than new markerno
Deleting existing Place
    Get existing  markerno
    Decrement all existing markernos greater than that number
    
Ajax function to update server data
Refresh Markers
