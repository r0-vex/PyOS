#iloveyou#i love you more!
#rohith=True
#while True:
    #if not rohith:
     #   break
    #print("I LOVE YOU")

#madam np it won't stop running.........
#😁😁#i cant run it .wait 
def respond(text):
    text=text.lower().strip()
    if"hello" in text or "hi" in text:
        return "hey there!"
    if"hey" in text or "yoo" in text:
        return"sup buddy"
    if"dude" in text or "bro" in text:
        return"wassup"
    if"how are you" in text:
        return "i am good,how about you?"
    if"yea good" in text or "yea not bad" in text:
        return"alr glad to hear"
    if"good" in text or "not bad" in text:
        return"sounds alr"
    if"can we talk" in text or "i want to talk" in text:
        return " oh my dear,i am all ears"
    if"problem" in text or "os is not working" in text:
        return"list it out"
    if"wifi" in text or "network" in text:
        return"networking problems?maybe your interface is down or there are DNS/IP conflicts"
    if"disk"in text or "storage" in text:
        return "disk issues detected?check if parritions are full, or filesystem errors exist"
    if"check memory" in text or"cpu" in text:
        return "try:'top' or 'htop' to see CPU load and process usage."
    if"check disk" in text:
        return "try:'df-h' to see disk usage or 'fsck' for filesystem check."
    if"slow" in text or "lag" in text:
        return"hmm,your os might have memory or CPU issues,check running processes or high memory"
    if"crash" in text or "error" in text:
        return"startup issues could be due to kernel panic, missing init files, or misconfigured services"
    if"bye" in text:
        return"see ya"
    return"hmm i didnt get that.say it differently"
def main():
    print("chatbot online.type'bye'to exit.\n")
    while True:
        user_input=input("you:")
        if "bye" in user_input.lower():
            print("bot:see ya")
            break
        reply=respond(user_input)
        print(f"bot:{reply}")
if __name__=="__main__":
    main()