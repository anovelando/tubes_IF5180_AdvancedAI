import random

def movement(myPlayer):
    while True:
        print("Chosen move: ", end="")
        move = select_movement(myPlayer).upper()
        if move in ["W", "A", "S", "D"]:
            print(move)
            break

    return move

def select_movement(myPlayer):
    '''
    Ubahlah algoritma perpindahan yang dipilih player dengan mengubah fungsi ini.
    Untuk saat ini fungsi masih mengembalikan random
    Keluaran dari fungsi ini adalah arah gerakan player:
        "W" --> player akan berpindah ke atas
        "A" --> player akan berpindah ke kiri
        "S" --> player akan berpindah ke bawah
        "D" --> player akan berpindah ke kanan
    Silahkan tambahkan atribut/ method di kelas Player jika dibutuhkan, tapi jangan menghapus/ mengganti atribut/ kelas yang sudah ada.
    '''
    '''
    Change the player's selected movement algorithm by changing this function.
    For now, the function still returns random.
    The output of this function is the player's movement direction:
        "W" --> player will move up
        "A" --> player will move to the left
        "S" --> player will move down
        "D" --> player will move to the right
    You can add attributes and/or methods in class Player if needed, but do not delete or replace existing attributes and classes.
    '''
    # return random.choice(["W", "A", "S", "D"])

    myPlayer.update_knowledge()

    return myPlayer.forward()
