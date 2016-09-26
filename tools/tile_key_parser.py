
    
def get_tilesheet_key(file):
    
    f = open('assets/tilesheets/keys/%s.txt' % file, 'r')
    
    tilesheet_key = {}

    for line in f:

        key, end = get_key(line)
        value = get_value(line, end)
        tilesheet_key[key] = value

    f.close()
    return tilesheet_key
    
    
def get_key(line):
    
    letters = []
    end = 0
    
    for letter in line:
        if letter == ' ':
            break
        else:
            letters.append(letter)
            end += 1
            
    key = ''.join(letters)
    
    return key, end
    
    
def get_value(line, end):
    
    tup = []
    value = []
    state = 'one'
    
    for letter in line[end+1:-1]:
        if state == 'one' and letter != ',':
            value.append(letter)
        elif state == 'one' and letter == ',':
            v1 = int(''.join(value))
            tup.append(v1)
            state = 'two'
            value = []
        elif state == 'two':
            value.append(letter)
    
    v2 = int(''.join(value))
    tup.append(v2)
    value = tuple(tup)
    
    return value


# a = 'avatar_key'
# m = 'monster_key'
# t = get_tileset_key(a)
