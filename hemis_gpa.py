

def calculate(data):
    s = 0
    cnt = 0 
    for i in data:
        s += i['k']*i['u'] 
        cnt += i['k']
    print(s,cnt)
    print(s/cnt)
data = [
    {
        'k':4,
        'u':4
    },
    {
        'k':2,
        'u':4
    },
    {
        'k':4,
        'u':4
    },
    {
        'k':8,
        'u':5
    },
    {
        'k':6,
        'u':4
    },
    {
        'k':6,
        'u':4
    },

    {
        'k':4,
        'u':3
    },
    {
        'k':2,
        'u':4
    },
    {
        'k':4,
        'u':4
    },
    {
        'k':4,
        'u':4
    },
    {
        'k':4,
        'u':3
    },
    {
        'k':6,
        'u':4
    },
    {
        'k':6,
        'u':4
    },
    {
        'k':6,
        'u':4
    },
    {
        'k':6,
        'u':4
    },
    {
        'k':6,
        'u':5
    },
    {
        'k':6,
        'u':3
    },
    {
        'k':6,
        'u':4
    },

    {
        'k':6,
        'u':5
    },
    {
        'k':6,
        'u':5
    },
    {
        'k':6,
        'u':5
    },
    {
        'k':6,
        'u':5
    },
    {
        'k':6,
        'u':5
    },

    {
        'k':6,
        'u':4
    },
    {
        'k':6,
        'u':5
    },
    {
        'k':6,
        'u':5
    },
    {
        'k':6,
        'u':5
    },
    {
        'k':2,
        'u':4
    },
    {
        'k':4,
        'u':5
    },

    {
        'k':6,
        'u':4
    },
    {
        'k':6,
        'u':5
    },
    {
        'k':6,
        'u':4
    },
    {
        'k':6,
        'u':5
    },
    {
        'k':4,
        'u':4
    },
    {
        'k':0,
        'u':3
    },
    {
        'k':0,
        'u':5
    },
    {
        'k':2,
        'u':5
    },

    {
        'k':6,
        'u':5
    },
    {
        'k':6,
        'u':4
    },
    {
        'k':6,
        'u':4
    },
    {
        'k':6,
        'u':4
    },

    {
        'k':6,
        'u':5
    },
    {
        'k':6,
        'u':4
    },
    {
        'k':6,
        'u':4
    },

    # {
    #     'k':18,
    #     'u':5
    # },
    
]

calculate(data)
print(len(data))