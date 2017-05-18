def likes(names):
    n = len(names)
    return {
        0: 'no one likes this',
        1: '{} likes this',
        2: '{} and {} like this',
        3: '{}, {} and {} like this',
        4: '{}, {} and {others} others like this'
    }[min(4, n)].format(*names[:3], others=n-2)

if __name__ == "__main__":
    print likes(["jack"])
    print likes(["jack", "maria"])
    print likes(["jack", "sora", "maria"])
