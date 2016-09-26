

def make_animated_tile_sheet():
    
    f = open('assets/tilesets/key.txt','r')
    new = open('assets/tilesets/keys/new_key.txt', 'a')
    w = 19

    count = 0
    row = 0
    col = 0
    y = 0

    for line in f:
        
        tag = line[:-1]
        if tag == 'blank':
            count += 1
            continue
        
        if count >= w:
            row = (count / w)
            y = row * 2
            col = count - (row * w)
        else:
            col = count
            
        new.write('%s1 %d,%d\n' % (tag, col, y))
        new.write('%s2 %d,%d\n' % (tag, col, y+1))
        
        count += 1

    f.close()
    new.close()

def make_tile_sheet():
    
    f = open('assets/tiles/key.txt','r')
    new = open('assets/tiles/keys/new_key.txt', 'a')
    w = 19

    count = 0
    row = 0
    col = 0

    for line in f:
        
        tag = line[:-1]
        if tag == 'blank':
            count += 1
            continue
        
        if count >= w:
            row = (count / w)
            col = count - (row * w)
        else:
            col = count
            
        new.write('%s %d,%d\n' % (tag, col, row))
        
        count += 1

    f.close()
    new.close()
    
make_tile_sheet()
