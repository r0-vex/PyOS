music_library=[["BlackPink",["HopeNot","IceCream","Whistle"]],["BritneySpears",["Toxic","GimmeMore","Opps i did it again"]],["TaylorSwift",["Lovestory","Enchanted","Red"]],["Anirudh",["Badass","Marana Mass","Ordinary Person"]]]
def Artists():
    print("\nArtists in Library:")
    for mu in music_library:
        print(" -",mu[0])
    print()
def show_songs(Artist_name):
    for mu in music_library:
        if mu[0].lower()==Artist_name.lower():
            for song in mu[1]:
                print(" -",song)
            return
    print("\nartist not found\n")
def menu():
    print("1.Show artists")
    print("2.Display artist songs")
    print("3.Exit")
while True:
    menu()
    try:
        Select=int(input("\nPyOS:/home/user/apps/music_player/option> "))
        if Select==1:
            Artists()
        elif Select==2:
            name_of_Artist=input("\nPyOS:/home/user/apps/music_player/artist>")
            show_songs(name_of_Artist)
        elif Select==3:
            print("\nExiting the music player!!\n")
            break
        else:
            print("invalid choice")
    except ValueError:
        print("Enter a number")
        
