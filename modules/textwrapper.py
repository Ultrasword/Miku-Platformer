def textwrap(text, limit):
    l = text.split()
    output = []
    string = ""
    lim = 0
    for word in l:
        wlen = len(word)
        if wlen + 1 > limit:
            if len(string) != 0:
                output.append(string)
            lim = 0
            output.append(str(word[:limit]))
            string = word[limit::]
            lim += len(word[limit::])
        else:
            if lim + wlen > limit:
                output.append(string)
                string = word[:limit]
                lim = len(word[:limit])
            else:
                string += word
                lim += len(word)
        string += " "
        lim += 1
    output.append(string)
    return output
